from django.shortcuts import render

# Create your views here.
import os
import requests
from django.http import HttpResponse, JsonResponse
import json

from friendship.models import Friend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from trail.models import Trail
from reviews.models import Reviews, ReviewImages
try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class TrailViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["POST"], detail=True)
    def add_trail(self, request):

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            check_trail_added = Trail.objects.filter(user_id=request.user, restaurant_id=body['restaurant_id'])
            if check_trail_added:
                success_response = {'success': True, 'Message': 'Cannot add previously added trail'}
                return JsonResponse(success_response)
            else:
                trail = Trail.objects.create(name=body['name'],
                                           latitude=body['latitude'],
                                           image_url=body['image_url'],
                                           address=body['address'] if "address" in body else "",
                                           city=body['city'] if "city" in body else "",
                                           state=body['state'] if "state" in body else "",
                                           country=body['country'] if "country" in body else "",
                                           zipcode=body['zipcode'] if "zipcode" in body else "",                                           
                                           phone=body['phone'] if "phone" in body else "",
                                           price=body['price'] if "price" in body else "",
                                           restaurant_id=body['restaurant_id'],
                                           longitude=body['longitude'],
                                           user_id=request.user)
                trail.save()
                success_response = {'success': True, 'Message': 'Trail Added Successfully'}
                return JsonResponse(success_response)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    @action(methods=["GET"], detail=True)
    def get_trail(self, request):
        try:
            user_id = request.GET['uuid'] if 'uuid' in request.GET else request.user.uuid
            all_trails = Trail.objects.filter(user_id=user_id).order_by('created_on').reverse().values()
            friends = Friend.objects.filter(from_user_id=user_id).values()
            success_response = {'success': True, 'trails': list(all_trails), 'trailCount': len(list(all_trails)), 'friendCount': len(list(friends))}
            return JsonResponse(success_response)
        except Exception as e:
            return JsonResponse({"error": str(e)})

    @action(methods=["delete"], detail=True)
    def delete_trail(self, request):
        if 'visit_id' in request.GET:
            try:
                trail_tobe_deleted = Trail.objects.filter(visit_id=request.GET['visit_id'] )
                if trail_tobe_deleted:
                    trail_tobe_deleted.delete()
                    success_response = {'success': True, 'Message': 'Trail Deleted Successfully!!'}
                    return JsonResponse(success_response)
                else:
                    success_response = {'success': False, 'Message': 'Trail Selected is not present' }
                    return JsonResponse(success_response)
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            success_response = {'success': False, 'Message': 'Missing parameters! Send Visit ID'}
            return JsonResponse(success_response)

    @action(methods=["GET"], detail=True)
    def get_visited_friends(self, request):
        if 'restaurant_id' in request.GET:
            try:
                user_id = request.user.uuid
                restaurant = request.GET['restaurant_id']
                friend_IDS = Friend.objects.filter(from_user_id=user_id).values_list('to_user_id')
                friend_trails = Trail.objects.filter(user_id__in=friend_IDS, restaurant_id=restaurant).values_list('user_id')
                users = user_model.objects.filter(uuid__in=friend_IDS).values()

                for friend in list(users):
                    print(friend)
                    review = Reviews.objects.filter(restaurant_id=restaurant, user_id=friend['uuid']).values()
                    friend['reviews']=list(review)
                    reviewIDS = Reviews.objects.filter(restaurant_id=restaurant, user_id=friend['uuid']).values_list('review_id', flat=True)
                    images = ReviewImages.objects.filter(review_id__in=reviewIDS).values_list('images_url',flat=True)
                    friend['reviewImages']=list(images)
                
                user_trail = Trail.objects.filter(user_id=user_id, restaurant_id=restaurant).values()
                user_has_visited = False
                if user_trail:
                    user_has_visited = True
                
                success_response = {'success': True, 'visitedFriends': list(users), 'hasUserVisited': user_has_visited}
                return JsonResponse(success_response)
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            success_response = {'success': False, 'Message': 'Missing parameters! Send restaurant ID'}
            return JsonResponse(success_response)

















