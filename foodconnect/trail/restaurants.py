import os
import requests
from django.http import HttpResponse, JsonResponse
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.conf import settings
from trail.models import Trail

class RestaurantViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["GET"], detail=True)
    def get_restaurants(self, request, limit=25, offset=0):

        if 'lat' in request.GET and 'long' in request.GET:
            parameters = {
                'latitude': request.GET['lat'],
                'longitude': request.GET['long'],
                'offset': request.GET.get("offset", offset),
                'limit': limit,
                'term': 'restaurants'
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
    
    def recommend_restaurants(self, request):
        user_id = request.user.uuid
        user_trail = Trail.objects.filter(user_id=user_id).values_list('restaurant_id', flat=True)
        restaurnatsIDS=self.get_recommendations(list(user_trail))
        restaurants=[]
        if len(restaurnatsIDS)>0:
            for ids in restaurnatsIDS:
                response: JsonResponse=self.get_restaurant_by_ID(ids=ids)
                jResponse = json.loads(response.content.decode('utf-8'))
                restaurants.append(jResponse['restaurants'])
            success_response = {'success': True, 'restaurants': {'businesses':restaurants}}
            return JsonResponse(success_response)
        else:
            return self.get_restaurants(request,5,60)
    
    def get_recommendations(self,filter_input,n=5):
        labelEncodedIDS=[]
        for restaurantId in filter_input:
            try:
                transformed=settings.LE.transform([restaurantId])
                labelEncodedIDS.append(transformed)
            except:
                continue

        indices1=[]
        if len(labelEncodedIDS)>0:
            for i in labelEncodedIDS:
                distances , indices = settings.KNN.kneighbors(settings.CSR[i],n_neighbors=10)
                indices = indices.flatten()
                indices= indices[1:]
                indices1.extend(indices)
                recommendedIDs=list(set(settings.LE.inverse_transform(indices1)))
            recommendedIDs=recommendedIDs[0:n]
        else:
            recommendedIDs=[]
        return recommendedIDs
        

    @action(methods=["GET"], detail=True)
    def get_restaurant_by_ID(self,request=None, ids=None):
        if ids:
            restaurant_id=ids
        elif request and 'restaurant_id' in request.GET:
            restaurant_id=request.GET['restaurant_id']

        if restaurant_id:
            url =  'https://api.yelp.com/v3/businesses/'+ restaurant_id
            api_key = os.getenv("YELP_API_KEY")
            headers = {'Authorization': 'bearer %s' % api_key}
            response = requests.get(url=url, headers=headers)
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