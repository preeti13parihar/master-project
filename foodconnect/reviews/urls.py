from django.conf.urls import url

from .reviews import ReviewViewSet
from .views import ImageUploader

add_review = ReviewViewSet.as_view({
    'post': 'add_review'
})

get_review = ReviewViewSet.as_view({
    'get': 'get_review'
})



urlpatterns = [
    url(r'^upload', ImageUploader.as_view(), name='file-upload'),
    url(r'^addReview', add_review , name='add_review'),
    url(r'^getReview', get_review , name='get_review'),
]