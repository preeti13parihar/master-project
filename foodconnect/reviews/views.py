from reviews.serializers import ImageSerialzer, ProfileImageSerialzer
import json
from .utils import upload_image
from .models import Images, ProfileImage
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.permissions import AllowAny
from django.http.response import JsonResponse
from rest_framework.response import  Response
from rest_framework.parsers import MultiPartParser, FormParser

try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

class ImageUploader(mixins.ListModelMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    serializer_class = ImageSerialzer
    queryset = Images.objects.all()

    def post(self, request):
        try:
            # folder = "reviews"
            if not request.FILES.get("file", None):
                return Response({"msg": "Invalid key for file upload, expecting 'file'"}, status=status.HTTP_400_BAD_REQUEST)

            # IsProfileImage = False
            # if ("profile" in request.POST) and request.POST["profile"] == "true":
            #     IsProfileImage = True
            #     folder = "profiles"
            #     file_serialzer = ProfileImageSerialzer(data=request.data)
            # else:
            #     file_serialzer = ImageSerialzer(data=request.data)

            # print(file_serialzer)
            request.data["description"] = "profile pic"
            file_serialzer = ProfileImageSerialzer(data=request.data, partial=True)
            uuid = str(request.user.uuid)
            url = upload_image(request.FILES['file'], "profiles/" + uuid)

            if file_serialzer.is_valid():
            #     print(file_serialzer["description"].value)

                desc = file_serialzer["description"].value
            #     if IsProfileImage:
            #         image = ProfileImage.objects.create(user_id=request.user, url=url, description=desc)
            #     else:
            #         if "review_id" not in file_serialzer.data:
            #             return Response({"msg": "Please provide review_id to upload review images."}, status=status.HTTP_400_BAD_REQUEST)

            #         review_id = file_serialzer["review_id"].value
            #         image = Images.objects.create(review_id=review_id, url=url, description=desc)

                image = ProfileImage.objects.create(user_id=request.user, url=url, description=desc)
                image.save()
                user = user_model.objects.get(uuid=uuid)
                user.image = url
                user.save()
                obj = model_to_dict(image)
                return Response(obj, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            raise Exception("Error while uploading image: " + str(e))    
    

    def get(self, request, *args, **kwargs):
        all = Images.objects.all()
        return self.list(request, *args, **kwargs)