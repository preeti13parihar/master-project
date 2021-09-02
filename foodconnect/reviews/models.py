import uuid
from authentication.models import User
from trail.models import Trail
from django.db import models


class Reviews(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Trail, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(max_length=500)
    recommended_dishes = models.CharField(max_length=200)

    def __str__(self):
        return self.user_id.first_name + ' -> ' + self.restaurant_id.name


class Images(models.Model):
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ReviewImages(Images):
    review_id = models.ForeignKey('Reviews', on_delete=models.CASCADE)