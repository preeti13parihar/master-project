from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from authentication.models import User

class UserAdminView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
    