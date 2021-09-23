from django.conf.urls import url
from .views import FriendsList, FriendViewSet
from authentication.views import UserSearchViewSet


add_friend = FriendViewSet.as_view({
    'post': 'add_friend'
})

accept_request = FriendViewSet.as_view({
    'get': 'accept_request'
})

reject_request = FriendViewSet.as_view({
    'get': 'reject_request'
})

cancel_request = FriendViewSet.as_view({
    'get': 'cancel_request'
})

list_requests = FriendViewSet.as_view({
    'get': 'list_requests'
})


list_friends = FriendViewSet.as_view({
    'get': 'list_friends'
})


urlpatterns = [
    url(r'^list', list_friends, name='list_friends'),
    url(r'^list/(?P<user_id>\w+)', list_friends, name='list_friends'),
    url(r'^add', add_friend, name='add_friend'),
    url(r'^accept/(?P<friendship_request_id>\d+)', accept_request, name='accept_request'),
    url(r'^reject/(?P<friendship_request_id>\d+)', reject_request, name='reject_request'),
    url(r'^cancel/(?P<friendship_request_id>\d+)', cancel_request, name='cancel_request'),
    url(r'requests', list_requests, name='list_requests'),
    url(r'^search', UserSearchViewSet.as_view({'get':'search_user'}), name='search'),

]