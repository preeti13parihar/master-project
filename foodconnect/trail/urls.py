from trail import restaurants
from django.conf.urls import url

urlpatterns = [
    url(r'^restaurants', restaurants.get_restaurants, name='list_restaurants')
]
