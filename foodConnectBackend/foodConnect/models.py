import uuid

from django.db import models
from django.core.validators import *


# Create your models here.

class Customer(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name


class RestaurantTrail(models.Model):
    visit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    restaurant_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    price = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id.first_name + ' -> ' + self.name


class Reviews(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey('RestaurantTrail', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=200)
    recommended_dishes = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id.first_name + ' -> ' + self.restaurant_id.name


class Friends(models.Model):
    connection_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    friend_id = models.ForeignKey('Customer', db_column='user_id', on_delete=models.CASCADE, related_name='friend_of')
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id.first_name + ' -> ' + self.friend_id.first_name


class ReviewImages(models.Model):
    review_id = models.ForeignKey('Reviews', on_delete=models.CASCADE)
    imagesUrl = models.CharField(max_length=200)
