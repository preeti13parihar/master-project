import base64
import binascii
from rest_framework.authentication import BaseAuthentication
from authentication.middleware import helpers
from rest_framework.exceptions import AuthenticationFailed

class AwsRestAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # This is where we will extract information about the incoming access token from the user,
        # and decide whether or not they are authenticated

        user, access_token, refresh_token, err = helpers.process_request(request)

        # TODO: Potentially create a mixin for views overriding the .finalise_response method to ensure if we
        # end up with a new access token as part of this process, we are able to set it in the response
        #
        # Need some way of setting a new access token or refresh token in the final response

        return user, access_token
