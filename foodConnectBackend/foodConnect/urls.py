from django.conf.urls import url
from django.urls import path
from . import restaurants

urlpatterns = [
    path('restaurants/', restaurants.get_restaurants),
    ]