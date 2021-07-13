# This will validate an incoming token and ensure that it is valid, and refresh it if required
#
# It will either return a new access token if it needed to refresh the existing one, None if the token
# was validated and didn't need to be refreshed, or raise an Exception if it can't validate the token
from os import urandom

import base64
import datetime
import json
import jwt
import binascii
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings
from authentication import utils
from authentication.cognito import constants, actions
from authentication.utils import PublicKey


def validate_token(access_token, refresh_token=None):
    try:
        header, payload = decode_token(access_token)
    except Exception as ex:
        # Invalid token or token we can't decode for whatever reason
        raise Exception("Invalid token")

    public_keys = utils.get_public_keys()

    [matching_key] = [key for key in public_keys['keys'] if key['kid'] == header['kid']]

    if matching_key is None:
        raise Exception("Invalid token public key")
    else:
        # Verify signature using the public key for this pool, as defined the the AWS documentation
        decode = jwt.decode(access_token, PublicKey(matching_key).pem, algorithms=[header['alg']],
                            options={'verify_exp': False})
        pass

    # TODO: Documentation says aud should be the key, but this doesn't exist and client_id has the data aud
    # should have
    #
    # Verify that the audience matches the Cognito app ID, as defined by the AWS documentation
    if payload['client_id'] != constants.CLIENT_ID:
        raise Exception("Invalid token audience")

    # Verify that the issuer matches the URL for the Cognito user pool, as defined by the AWS documentation
    if payload['iss'] != "https://cognito-idp." + constants.POOL_ID.split("_", 1)[0] + ".amazonaws.com/" \
            + constants.POOL_ID:
        raise Exception("Invalid token issuer")

    # Verify that the token is either not expired, or if expired, that we have a refresh token to refresh it
    if payload['exp'] <= datetime.datetime.timestamp(datetime.datetime.utcnow()):
        if not refresh_token:
            # The current access token is expired and no refresh token was provided, authentication fails
            raise Exception("The access token provided has expired. Please login again.")
        else:
            # This token is expired, potentially check for a refresh token? Return this token in the auth return
            # variable?
            result = actions.initiate_auth(payload['username'], constants.REFRESH_TOKEN_FLOW,
                                           refresh_token=refresh_token)

            if result['AuthenticationResult']:
                # Return the freshly generated access token as an indication auth succeeded but a new token was
                # required
                #
                # TODO: DON'T return refresh token here, for methods that require a refresh token we should implement
                # them somewhere else, or differently
                return result['AuthenticationResult']['AccessToken'], refresh_token
            else:
                # Something went wrong with the authentication
                raise Exception("An error occurred while attempting to refresh the access token")
    else:
        # The token validated successfully, we don't need to do anything else here
        return None, None


def generate_csrf():
    random_bytes = urandom(64)
    csrf_token = base64.b64encode(random_bytes).decode('utf-8')

    return csrf_token


def decode_token(access_token):
    token_parts = access_token.split(".")

    header = json.loads(
        base64.b64decode(token_parts[0] + "=" * ((4 - len(token_parts[0]) % 4) % 4)).decode('utf-8'))
    payload = json.loads(
        base64.b64decode(token_parts[1] + "=" * ((4 - len(token_parts[1]) % 4) % 4)).decode('utf-8'))

    return header, payload


def get_authorization_header(request, name="HTTP_AUTHORIZATION"):
    try:
        auth = request.META.get(name, None)  
        if not auth:
            return AuthenticationFailed("No auth header found !!!")

        # if isinstance(auth, str):
        #     # Work around django test client oddness
        #     auth = auth.encode('iso-8859-1')
        return auth.split()
    except Exception as e:
        raise AuthenticationFailed("Error: " + str(e))


def authenticate_credentials(self, userid, password, request=None):
    """
    Authenticate the userid and password against username and password
    with optional request for context.
    """
    credentials = {
        get_user_model().USERNAME_FIELD: userid,
        'password': password
    }
    user = authenticate(request=request, **credentials)

    if user is None:
        raise AuthenticationFailed(_('Invalid username/password.'))
    if not user.is_active:
        raise AuthenticationFailed(_('User inactive or deleted.'))

    return (user, None)


def get_userid_password_from_header(request, prefix="basic", name="HTTP_AUTHORIZATION"):
    try:
        auth = get_authorization_header(request, name)
        if isinstance(auth, Exception):
            return None, None, auth
            
        if not auth or auth[0].lower() != prefix:
            return None, None, auth

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            return None, None, AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            return None, None, AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode('utf-8')
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode('latin-1')
            auth_parts = auth_decoded.partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            return None, None, AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        return userid, password, None
            
    except Exception as e:
        return None, None, Exception("Authentication failed, no authorization header found!!!")


def process_request(request):

    if settings.USE_CSRF:
        try:
            csrf_token_cookie = request.COOKIES.get('csrftoken')
            csrf_header = request.META['HTTP_CSRFTOKEN']

            if csrf_token_cookie != csrf_header:
                return None, None, None, Exception("CSRF Verification failed")
        except Exception as ex:
            return None, None, None, Exception("CSRF verification failed")
    
    try:
        access_token = request.META.get('HTTP_ACCESSTOKEN', None)
        try:
            refresh_token = request.META.get('HTTP_REFRESHTOKEN', None)
        except Exception as ex:
            # A refresh token doesn't have to be passed in, it's optional to auto renew access token
            pass

    except Exception as ex:
        return AnonymousUser(), None, None, None


    if not access_token or not refresh_token:
        # Need to have this to authenticate, error out
        return None, None, None, Exception("No valid tokens were found in the request")
    else:

        new_access_token, new_refresh_token = validate_token(access_token, refresh_token)
        if not new_access_token:
            new_access_token = access_token

        if not new_refresh_token:
            new_refresh_token = refresh_token

        header, payload = decode_token(access_token)

        try:
            user = get_user_model().objects.get(username=payload['username'])
        except Exception as ex:

            if settings.AUTO_CREATE_USER:
                
                aws_user = actions.admin_get_user(payload['username'])

                user_attributes = {k: v for dict in [{d['Name']: d['Value']} for d in aws_user['UserAttributes']]
                                   for k, v in dict.items()}

                user = get_user_model().objects.create(uuid=payload["sub"], username=payload['username'], email=user_attributes['email'],
                                                       first_name=user_attributes['given_name'],
                                                       last_name=user_attributes['family_name'])

                user.save()
            else:
                return AnonymousUser, None, None, None

        return user, new_access_token, new_refresh_token, None
        


def create_or_get_user(access_token):
        header, payload = decode_token(access_token)

        try:
            user = get_user_model().objects.get(username=payload['username'])
        except Exception as ex:
            aws_user = actions.admin_get_user(payload['username'])

            user_attributes = {k: v for dict in [{d['Name']: d['Value']} for d in aws_user['UserAttributes']]
                                for k, v in dict.items()}

            user = get_user_model().objects.create(uuid=payload["sub"], username=payload['username'], email=user_attributes['email'],
                                                    first_name=user_attributes['given_name'],
                                                    last_name=user_attributes['family_name'])

            user.save()

        return user
