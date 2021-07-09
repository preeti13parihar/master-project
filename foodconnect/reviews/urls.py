from django.conf.urls import url
from .views import ImageUploader

urlpatterns = [
    url(r'^upload', ImageUploader.as_view(), name='file-upload'),
]