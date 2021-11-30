import os
import json
import requests
from authentication.cognito.base import AppException, CognitoException
from django.conf import settings
from authentication.middleware import helpers
from django.http import JsonResponse, HttpResponse

from utils import log

logger = log.get_logger(__name__)


class AwsDjangoMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        path = request.get_full_path()
        path = path.strip("/")
        path = os.path.basename(path)
        try:
            if path in ["login", "signup", "confirm_signup", "csrf", "forgot_password", "confirm_forgot_password", "healthz"]:                
                r = self.get_response(request)
                # logger.info(r.content)
                return r
            user, token, refresh_token, err = helpers.process_request(request)
            if err:
                return JsonResponse({"error": str(err)}, status=400)

            request.user = user
            response = self.get_response(request)
            
            if isinstance(response, Exception):
                raise response
            elif isinstance(response, CognitoException):
                raise response

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

        except Exception as e:
            logger.error(str(e))

            if isinstance(e, CognitoException) or isinstance(e, AppException) or isinstance(e.args[0], dict):
                return JsonResponse(e.args[0], status=e.status)

            return JsonResponse({"error": str(e)}, status=400)            
            # return HttpResponse(str(e))


    def process_request(self, request):
        pass


    def process_exception(self, request, exception):
        logger.error(str(exception))
        
        if isinstance(exception, CognitoException) or isinstance(exception, AppException):
            return JsonResponse(exception.args[0], status=exception.status)

        return JsonResponse({"error": str(exception)}, status=400)