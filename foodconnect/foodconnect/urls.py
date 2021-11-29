from django.http.response import JsonResponse
from foodconnect.settings import URL_PREFIX
from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.urls import path
from django.conf.urls import include, url
from django.http import JsonResponse
from friends import views
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

router = routers.DefaultRouter()
router.register(r'^friends', views.FriendViewSet, basename='friends')

@api_view(['GET'])
@permission_classes((AllowAny, ))
def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    url(settings.URL_PREFIX, include([
        url(r'^admin/', admin.site.urls),
        # Custom apps URLS
        url(r'^auth/', include('authentication.urls')),
        url(r'^foodzone/', include('foodzone.urls')),
        url(r'^reviews/', include('reviews.urls')),
        # url(r'^', include(router.urls)),
        url(r'^friends/', include('friends.urls')),
        url(r'^trail/', include('trail.urls')),
        url(r'^healthz/', health),
        # url(r'^connections/', include('friends.urls'))
    ])),
    # path('admin/', admin.site.urls),

    # path('auth/login', views.initiate_auth),
    # path('auth/logout', views.sign_out),
    # path('auth/signup', views.sign_up),
    # path('auth/forgot_password', views.forgot_password),
    # path('auth/confirm_signup', views.confirm_sign_up),
    # path('auth/confirm_login', views.respond_to_auth_challenge),
    # path('auth/confirm_forgot_password', views.confirm_forgot_password),
    # path('auth/generate_csrf', views.get_csrf),
    # path('/', views.get_csrf),
    # path('auth/generate_csrf', views.get_csrf),
]
