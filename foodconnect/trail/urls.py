from trail import restaurants
from django.conf.urls import url

from trail.restaurants import RestaurantViewSet
from trail.views import TrailViewSet

get_restaurants = RestaurantViewSet.as_view({
    'get': 'get_restaurants'
})

add_trail = TrailViewSet.as_view({
    'post': 'add_trail'
})

get_trail = TrailViewSet.as_view({
    'get': 'get_trail'
})

delete_trail = TrailViewSet.as_view({
    'delete': 'delete_trail'
})

get_visited_friends = TrailViewSet.as_view({
    'get': 'get_visited_friends'
})

urlpatterns = [
    url(r'^restaurants', get_restaurants, name='list_restaurants'),
    url(r'^addTrail', add_trail, name='add_trail'),
    url(r'^getTrail', get_trail, name='get_trail'),
    url(r'^deleteTrail', delete_trail, name='delete_trail'),
    url(r'^getVisitedFriends', get_visited_friends, name='get_visited_friends'),

]
