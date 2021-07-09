import os
from authentication.cognito.base import CognitoException
from django.conf import settings
from authentication.middleware import helpers
from django.http import JsonResponse

    
class AwsDjangoMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # path = request.get_full_path()

        if os.path.basename(request.path) in ["login"]:
            return self.get_response(request)
        
        user, token, refresh_token, err = helpers.process_request(request)
        if err:
            return JsonResponse({"error": str(err)}, status=400)

        request.user = user
        response = self.get_response(request)
        
        if isinstance(response, Exception):
            return JsonResponse(response.args[0], status=response.status)


        if token:
            # TODO: Set the token in the response here as well? If the user hits here, they're still active
            http_only = settings.HTTP_ONLY_COOKIE
            secure = settings.SECURE_COOKIE
            
            response["HTTP_ACCESSTOKEN"] = token
            response["HTTP_REFRESHTOKEN"] = refresh_token

            response.set_cookie(key='AccessToken', value=token,
                                secure=secure, httponly=http_only)
            response.set_cookie(key="RefreshToken", value=refresh_token,
                                secure=secure, httponly=http_only)

        return response
    

    def process_request(self, request):
        pass
