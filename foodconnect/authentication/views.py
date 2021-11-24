import json

from datetime import timedelta
from django.conf import settings
from django.utils.datetime_safe import datetime
from django.db.models import Q

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from authentication.serializers import UserSearchSerializer
from authentication.models import User
from friendship.models import Friend
from authentication.cognito import helpers
from authentication.cognito import constants, actions
from django.contrib.auth import get_user_model

from authentication.cognito.base import CognitoException
from authentication.middleware.helpers import generate_csrf, get_userid_password_from_header, create_or_get_user


class UserSearchViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_url_kwarg = "name"

    @action(methods=["GET"], detail=True)
    def search_user(self, request):
        try:
            # frnd_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
            name = request.query_params.get('name', None)
            print("Name:", name)
            if not name:
                return JsonResponse([], safe=False)

            result = User.objects.filter(Q(last_name__icontains=name) | 
                            Q(first_name__icontains=name))
            print("Result", result)
            friends = Friend.objects.filter(to_user_id=request.user.uuid)
            print("Friends", friends)

            out = []
            # if not result:
            #     for f in friends:
            #         r = User.objects.get(uuid=f.to_user_id)
            #         d = {
            #                 "uuid": r.uuid,
            #                 "first_name": r.first_name,
            #                 "last_name": r.last_name,
            #                 "email": r.email,
            #                 "image_url": r.image,
            #                 "is_friend": True
            #             }
            #         out.append(d)
            #     return JsonResponse(out, safe=False)
                
            for r in result:
                d = {
                        "uuid": r.uuid,
                        "first_name": r.first_name,
                        "last_name": r.last_name,
                        "email": r.email,
                        "image_url": r.image,
                        "is_friend": False
                    }
                for f in friends:
                    if r.uuid == f.to_user_id:
                        d["is_friend"] = True

                out.append(d)
            # resp = UserSearchSerializer(result, many=True)
            # return JsonResponse(resp.data, safe=False)
            return JsonResponse(out, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})


@require_http_methods(['POST'])
def initiate_auth(request):
    try:
        userid, password, err = get_userid_password_from_header(request)
        if err:
            return err

        data = {}
        data["username"] = userid
        data["password"] = password

        # data = json.loads(request.body.decode('utf-8'))
        result = helpers.initiate_auth(data)

        if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
            access_token = result["AuthenticationResult"]["AccessToken"]
            refresh_token = result["AuthenticationResult"]["RefreshToken"]
            response = JsonResponse({
                "msg": "Welcome " + userid, 
                "access_token": access_token,
                "refresh_token": refresh_token
            })
            # response = redirect(to="homepage", permanent=True)
            response["HTTP_ACCESSTOKEN"] = access_token
            response["HTTP_REFRESHTOKEN"] = refresh_token

            token = response.get('HTTP_ACCESSTOKEN')
            refresh_token = response.get('HTTP_REFRESHTOKEN')

            response.set_cookie(key='AccessToken', value=token,
                                secure=settings.SECURE_COOKIE, httponly=settings.HTTP_ONLY_COOKIE)
            response.set_cookie(key="RefreshToken", value=refresh_token,
                                secure=settings.SECURE_COOKIE, httponly=settings.HTTP_ONLY_COOKIE)

            # user = create_or_get_user(access_token)
            return response
            
        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=500)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)


@require_http_methods(['POST'])
def sign_out(request):
    try:
        access_token = request.META["HTTP_ACCESSTOKEN"]
        # data = json.loads(request.body.decode('utf-8'))
        result = helpers.sign_out({"access_token": access_token})

        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)


@require_http_methods(['POST'])
def respond_to_auth_challenge(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        result = helpers.respond_to_auth_challenge(data)

        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)
    pass


@require_http_methods(['POST'])
def forgot_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        result = helpers.forgot_password(data)

        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)
    pass


@require_http_methods(['POST'])
def confirm_forgot_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        result = helpers.confirm_forgot_password(data)

        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)
    pass


@require_http_methods(['POST'])
def sign_up(request):
    try:
        userid, password, err = get_userid_password_from_header(request)
        if isinstance(err, Exception):
            return JsonResponse({"error": str(err)}, status=500)

        data = json.loads(request.body.decode('utf-8'))
        data["username"] = userid
        data["password"] = password
        result = helpers.sign_up(data)

        if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
            if "CodeDeliveryDetails" in result and (result["CodeDeliveryDetails"]["DeliveryMedium"] == "EMAIL"):
                msg = "We sent verification email to you at: " + result["CodeDeliveryDetails"]["Destination"]

            response = JsonResponse({
                "msg": msg
            })
            return response

        return JsonResponse(result)

    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)


@require_http_methods(['POST'])
def confirm_sign_up(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        result = helpers.confirm_sign_up(data)

        return JsonResponse(result)
    except CognitoException as ex:
        return JsonResponse(ex.args[0], status=ex.status)
    except ValueError as ex:
        return JsonResponse({"error": ex.args[0]}, status=400)


@require_http_methods(['GET'])
def get_csrf(request):
    csrf_token = generate_csrf()

    http_only = settings.HTTP_ONLY_COOKIE

    response = JsonResponse({"csrftoken": csrf_token})
    response.set_cookie(key='csrftoken', value=csrf_token,
                        secure=False, httponly=http_only, domain="localhost",
                        expires=datetime.now() + timedelta(days=30))

    return response


