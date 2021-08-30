import os
import requests
from django.http import HttpResponse, JsonResponse
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action


class RestaurantViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=True)
    def get_restaurants(self, request):

        if 'lat' in request.GET and 'long' in request.GET:
            parameters = {
                'latitude': request.GET['lat'],
                'longitude': request.GET['long'],
                'offset': request.GET.get("offset", 0),
                'limit': 50
            }

            url = 'https://api.yelp.com/v3/businesses/search'
            api_key = os.getenv("YELP_API_KEY")
            headers = {'Authorization': 'bearer %s' % api_key}
            response = requests.get(url=url, headers=headers, params=parameters)
            if response and response.status_code == 200:
                parsed = json.loads(response.text)
                success_response = {'success': True, 'restaurants': parsed}
                return JsonResponse(success_response)
            else:
                error_object = {'success': False, 'message': 'Error connecting to yelp', 'reason': response.reason,
                                'statusCode': response.status_code, 'error': response.text}
                return JsonResponse(error_object)
        else:
            error_object = {'success': False, 'message': 'Missing Parameters! Lat & Long required'}
            return JsonResponse(error_object)
