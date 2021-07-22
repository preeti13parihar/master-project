from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import permissions

from authentication.models import User
from authentication.serializers import UserSerializer, UpdateUserSerializer


class ProfileUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = "uid"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateUserSerializer
        return UserSerializer

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def get_object(self,):
        uid = self.kwargs["uid"]
        return get_object_or_404(User, uuid=uid)


# class ProfileDeleteAPI(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     lookup_url_kwarg = "uid"
