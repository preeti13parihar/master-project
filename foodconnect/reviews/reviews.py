from django.http import HttpResponse, JsonResponse
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from reviews.models import Reviews, ReviewImages
from reviews.serializers import ImageSerialzer, FileSerializer
from reviews.utils import upload_image
from reviews.views import ImageUploader

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=["POST"], detail=True)
    def add_review(self, request):
        try:
            body = request.data
            review = Reviews.objects.create(rating=body['rating'],
                                            review=body['review'],
                                            restaurant_id=body['restaurant_id'],
                                            recommended_dishes=body['recommended_dishes'],
                                            user_id=request.user)
            serializer_class = FileSerializer(data=body)
            if 'file' in request.FILES and serializer_class.is_valid():
                files = request.FILES.getlist('file')
                for f in files:
                    url = upload_image(f)
                    print(url)
                    reviewImages = ReviewImages.objects.create(review_id=review, images_url=url)
                    reviewImages.save()

            success_response = {'success': True, 'Message': 'Review Added Successfully'}
            return JsonResponse(success_response)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    def get_review(self, request):
        try:
            user_id = request.GET['uuid'] if 'uuid' in request.GET else request.user.uuid
            restaurant_id = request.GET['restaurant_id']
            reviews = Reviews.objects.filter(restaurant_id=restaurant_id, user_id=user_id).values()
            if reviews:
                images = ReviewImages.objects.filter(review_id=reviews[0]['review_id']).values('images_url')
                success_response = {'success': True, 'images': list(images), 'review': list(reviews)}
            else:
                success_response = {'success': True, 'images': list(), 'review': list()}
            return JsonResponse(success_response)
        except Exception as e:
            return JsonResponse({"error": str(e)})




