from django.shortcuts import render

# Create your views here.
import os
import requests
from django.http import HttpResponse, JsonResponse
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from trail.models import Trail


class TrailViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["POST"], detail=True)
    def add_trail(self, request):

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            trail=Trail.objects.create(name=body['name'],
                                       latitude=body['latitude'],
                                       image_url=body['image_url'],
                                       address=body['address'],
                                       city=body['city'],
                                       state=body['state'],
                                       country=body['country'],
                                       zipcode=body['zipcode'],
                                       phone=body['phone'],
                                       price=body['price'],
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
            user_id = request.user.uuid
            all_trails = Trail.objects.filter(user_id=user_id)
            all_trails_list = []
            for i in all_trails:
                all_trails_list.append(i.returnObject())
            success_response = {'success': True, 'trails': all_trails_list}
            return JsonResponse(success_response)
        except Exception as e:
            return JsonResponse({"error": str(e)})







