from django.db import models
from django.db.models import fields
from rest_framework import serializers
from friendship import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friend
        # exclude = ['name']
        fields = "__all__" #
        # fields = ("id", "created", "to_user", "from_user", "first_name", "last_name", "image_url")

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    
    def get_first_name(self, obj):
        user = User.objects.get(uuid=obj.to_user.uuid)
        return user.first_name

    def get_last_name(self, obj):
        user = User.objects.get(uuid=obj.to_user.uuid)
        return user.last_name

    def get_image_url(self, obj):
        user = User.objects.get(uuid=obj.to_user.uuid)
        return user.image


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FriendshipRequest
        fields = "__all__"
        # fields = ("to_user", "message", "first_name", "last_name", "image_url")

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    
    def get_first_name(self, obj):
        user = User.objects.get(uuid=obj["to_user"].uuid)
        return user.first_name

    def get_last_name(self, obj):
        user = User.objects.get(uuid=obj["to_user"].uuid)
        return user.last_name

    def get_image_url(self, obj):
        user = User.objects.get(uuid=obj["to_user"].uuid)
        return user.image


class FriendFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = '__all__'

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    
    def get_first_name(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.first_name

    def get_last_name(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.last_name

    def get_image_url(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.image


class FriendBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Block
        fields = '__all__'

    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    
    def get_first_name(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.first_name

    def get_last_name(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.last_name

    def get_image_url(self, obj):
        user = User.objects.filter(uuid=obj.from_user.uuid).first()
        return user.image
