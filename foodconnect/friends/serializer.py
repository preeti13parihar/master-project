from django.db import models
from django.db.models import fields
from rest_framework import serializers
from friendship import models


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friend
        fields = '__all__'
    

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FriendshipRequest
        fields = ("to_user", "message")


class FriendFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = '__all__'


class FriendBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Block
        fields = '__all__'

