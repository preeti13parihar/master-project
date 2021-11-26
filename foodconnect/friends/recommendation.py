import os
import requests
from django.http import HttpResponse, JsonResponse
import json
from reviews.models import Reviews

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from django.db.models import Q
from authentication.serializers import UserSerializer
from friendship.models import Friend
try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

class FriendRecommendationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer  

    @action(methods=["GET"], detail=True)
    def get_friend_recommendation(self, request):
        try:
            user_id = request.GET['uuid'] if 'uuid' in request.GET else request.user.uuid
            top_reviews = Reviews.objects.filter(user_id=user_id ,rating__range=(3, 5) ).values_list('restaurant_id', flat=True)
            friend_IDS = Friend.objects.filter(from_user_id=user_id).values_list('to_user_id',flat=True)
            if len(top_reviews) > 0:
                similar_users = Reviews.objects.filter(Q(restaurant_id__in=top_reviews) &  ~Q(user_id=user_id) & ~Q(user_id__in=list(friend_IDS)) & Q(rating__range=(3,5)) ).values_list('user_id', flat=True)
                if len(list(similar_users)) > 0:
                    user_details = user_model.objects.all().filter(uuid__in=list(similar_users)).values()
                else:
                    user_details = user_model.objects.filter(~Q(uuid__in=list(friend_IDS)) & ~Q(uuid=user_id)).values()[:5]
            else:
                user_details = user_model.objects.filter(~Q(uuid__in=list(friend_IDS)) & ~Q(uuid=user_id)).values()[:5]
            success_response = {'success': True, 'suggestions': list(user_details)}
            return JsonResponse(success_response)
        
        except Exception as e:
            return JsonResponse({"error": str(e)})
               
           

