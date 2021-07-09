from foodzone import views
from trail import restaurants
from django.conf.urls import url, include

urlpatterns = [
    url(r'^home', views.home, name='homepage'),
    url(r'^retaurants', restaurants.get_restaurants, name="get_restaurant")
]