from django.db.models import fields
from rest_framework import serializers
from .models import Images

class ImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('description',)


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)