from foodconnect.settings import URL_PREFIX
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    url(settings.URL_PREFIX, include([
        url(r'^admin/', admin.site.urls),
        # Custom apps URLS
        url(r'^auth/', include('authentication.urls')),
        url(r'^foodzone/', include('foodzone.urls')),
        url(r'^reviews/', include('reviews.urls')),
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
