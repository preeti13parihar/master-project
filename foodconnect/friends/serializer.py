from django.db import models
from django.db.models import fields
from rest_framework import serializers
from friendship import models


class FriendSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = models.Friend
        fields = "__all__" #("created", "to_user", "from_user", "first_name", "last_name")
    

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

