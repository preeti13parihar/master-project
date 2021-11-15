import uuid
from authentication.models import User
from django.db import models
from django.utils import timezone

class Trail(models.Model):
    visit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_id.first_name + ' -> ' + self.name
