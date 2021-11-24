from django.db.models import fields
from rest_framework import serializers
from .models import Images, ProfileImage

class ImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('description',)


class ProfileImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('description',)

class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)