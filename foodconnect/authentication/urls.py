from authentication import views
from authentication import profile
from django.conf.urls import url

urlpatterns = [
    # Exclude as not appropriate for this app?
    url(r'^login', views.initiate_auth, name='login'),
    url(r'^logout', views.sign_out, name='logout'),
    url(r'^signup', views.sign_up, name='signup'),
    url(r'^forgot_password', views.forgot_password, name='forgot_password'),
    url(r'^confirm_signup', views.confirm_sign_up, name='confirm_sign_up'),
    url(r'^confirm_login', views.respond_to_auth_challenge, name='confirm_login'),
    url(r'^confirm_forgot_password', views.confirm_forgot_password, name='confirm_forgot_password'),
    url(r'^generate_csrf', views.get_csrf, name='generate_csrf'),
    url(r'^profile/(?P<uid>[0-9a-f-]+)', profile.ProfileUpdateAPI.as_view(), name='profile'),
    url(r'^location/(?P<uid>[0-9a-f-]+)', profile.LocationUpdateAPI.as_view(), name='location'),
    # url(r'^profile/(?P<uid>[0-9a-f-]+)/delete', profile.ProfileDeleteAPI.as_view(), name='profile_delete'),
]