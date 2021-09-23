from reviews.serializers import ImageSerialzer
import json
from .utils import upload_image
from .models import Images
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse
from rest_framework.response import  Response
from rest_framework.parsers import MultiPartParser, FormParser


class ImageUploader(mixins.ListModelMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    serializer_class = ImageSerialzer
    queryset = Images.objects.all()

    def post(self, request):
        try:
            file_serialzer = ImageSerialzer(data=request.data)
            
            if not request.FILES.get("file", None):
                return Response({"msg": "Invalid key for file upload, expecting 'file'"}, status=status.HTTP_400_BAD_REQUEST)

            url = upload_image(request.FILES['file'])

            if file_serialzer.is_valid():
                desc = file_serialzer["description"].value
                image = Images.objects.create(user_id=request.user.uuid, url=url, description=desc)
                image.save()
                obj = model_to_dict(image)
                return Response(obj, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise Exception("Error while uploading image: " + str(e))    
    

    def get(self, request, *args, **kwargs):
        all = Images.objects.all()
        return self.list(request, *args, **kwargs)