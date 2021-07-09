from django.contrib.auth.models import User, AnonymousUser

from authentication.cognito.helpers import initiate_auth
from authentication.middleware import helpers as m_helpers

class AwsDjangoAuthentication:

    def authenticate(self, request, username=None, password=None):
        if username is None:
            user, _, _ = m_helpers.process_request(request)

            return user
        else:
            try:
                # We've received a username and password, do that authentication flow instead
                result = initiate_auth({"username":username, "password": password, "auth_flow": "USER_PASSWORD_AUTH"})

                return User.objects.get(email=username)
            except Exception as ex:
                # Either couldn't authenticate or user didn't exist, throw an error
                return AnonymousUser()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None