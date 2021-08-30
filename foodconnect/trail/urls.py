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

urlpatterns = [
    url(r'^restaurants', get_restaurants, name='list_restaurants'),
    url(r'^addTrail', add_trail, name='add_trail'),
    url(r'^getTrail', get_trail, name='get_trail')
]
