from authentication.serializers import UserSerializer
import json
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from friends import serializer
from friends.exceptions import AlreadyExistsError, AlreadyFriendsError
from friends.serializer import FriendSerializer, FriendRequestSerializer, FriendBlockSerializer, FriendFollowSerializer
from friendship.models import Friend, Follow, Block, FriendshipRequest


try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "friendship_request_id"

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FriendRequestSerializer

        return FriendSerializer

    @action(methods=["POST"], detail=True)
    def add_friend(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            to_user = user_model.objects.get(uuid=serializer.data["to_user"])
            from_user = request.user
            try:
                Friend.objects.add_friend(from_user, to_user)
            except Exception as e: # AlreadyExistsError as e:
                return JsonResponse({"msg": str(e)}, status=400)
            else:
                return JsonResponse({"msg": f"Friend request sent to {to_user} !!!"})
        else:
            return JsonResponse({"msg": "Bad request"})


    @action(methods=["GET"], detail=True)
    def accept_request(self, request, friendship_request_id=None):
        try:
            # frnd_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
            frnd_request = FriendshipRequest.objects.get(id=friendship_request_id)

            return JsonResponse({"Accepted": frnd_request.accept()})
        except Exception as e:
            if str(e) == "FriendshipRequest matching query does not exist.":
                return JsonResponse({"error": str(e)}, status=404)
            return JsonResponse({"error": str(e)}, status=500)


    @action(methods=["GET"], detail=True)
    def reject_request(self, request, friendship_request_id=None):
        try:
            # frnd_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
            print(friendship_request_id)
            frnd_request = FriendshipRequest.objects.get(id=friendship_request_id)

            return JsonResponse({"Rejected": True})
            
        except Exception as e:
            if str(e) == "FriendshipRequest matching query does not exist.":
                return JsonResponse({"error": str(e)}, status=404)
            return JsonResponse({"error": str(e)}, status=500)



    @action(methods=["GET"], detail=True)
    def cancel_request(self, request, friendship_request_id=None):
        try:
            frnd_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)
            return JsonResponse({"Cancelled": frnd_request.cancel()})
        except Exception as e:
            if str(e) == "FriendshipRequest matching query does not exist.":
                return JsonResponse({"error": str(e)}, status=404)
            return JsonResponse({"error": str(e)}, status=500)
            


    @action(methods=["GET"], detail=True)
    def list_requests(self, request):
        try:
            request_set = Friend.objects.requests(request.user)
            result =[]
            for request in request_set:
                result.append({
                    "id": request.id,
                    "from_user": str(request.from_user.uuid).replace("-",""),
                    "first_name": request.from_user.first_name,
                    "last_name": request.from_user.last_name,
                    "received_at": request.created
                })
                
            # serializer = FriendSerializer(request_set, many=True)
            # return Response(serializer.data)
            return Response(result)
        except Exception as e:
            return JsonResponse({"error": str(e)})


    @action(methods=["GET"], detail=True)
    def list_sent_requests(self, request):
        try:
            request_set = Friend.objects.sent_requests(request.user)
            result =[]
            for request in request_set:
                result.append({
                    "id": request.id,
                    "to_user": str(request.to_user.uuid).replace("-",""),
                    "first_name": request.to_user.first_name,
                    "last_name": request.to_user.last_name,
                    "sent_at": request.created
                })
                
            # serializer = FriendSerializer(request_set, many=True)
            # return Response(serializer.data)
            return Response(result)
        except Exception as e:
            return JsonResponse({"error": str(e)})


    @action(methods=["GET"], detail=True)
    def list_friends(self, request, user_id=None):
        """
            if user_id belongs to other user then it will list that user's friend list
            otherwise if it is missing it will return current logged in user's friend list 
        """
        try:
            if not user_id:
                user_id = request.user.uuid

            queryset = Friend.objects.filter(from_user_id=user_id)

            serializer = FriendSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return JsonResponse({"error": str(e)})


    @action(methods=["GET"], detail=True)
    def remove_friend(self, request, user_id=None):
        try:
            if not user_id:
                return JsonResponse({"msg": "Please provide friend uuid"}, status=404)

            print(user_id)
            print("Current user id:", request.user.uuid)
            friend = Friend.objects.get(Q(from_user_id__exact=user_id) & Q(to_user_id__exact=request.user.uuid))
            is_deleted = friend.delete()
            print(is_deleted)
            # is_deleted = friend.cancel()
            if is_deleted:
                return JsonResponse({"is_unfriend": True})

            return JsonResponse({"is_unfriend": is_deleted, "msg": "user couldn't be unfriend"}, status=500)
        except Exception as e:
            return JsonResponse({"error": str(e)})



class FriendsList(generics.ListCreateAPIView):
    queryset = Friend.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FriendRequestSerializer

        return FriendSerializer


    # def create(self, request, *args, **kwargs):
    @action(methods=["POST"], detail=True)
    def add_friend(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            to_user = user_model.objects.get(username=serializer.data["to_user"])
            from_user = request.user
            try:
                Friend.objects.add_friend(from_user, to_user)
            except Exception as e: # AlreadyExistsError as e:
                if str(e) == "Friendship already requested":
                    return JsonResponse({"msg": str(e)})
                else:
                    print("Error: ", str(e))
                    return JsonResponse({"msg": "Internal server error"})

            else:
                return JsonResponse({"msg": f"Friend request sent to {to_user} !!!"})
        else:
            return JsonResponse({"msg": "Bad request"})

    # @action(detail=True)
    # def add_friend(self, request, *args, **kwargs):
    #     body = json.loads(request.data)
    #     to_user = user_model.objects.get(username=body["to_user"])
    #     from_user = request.user
    #     try:
    #         Friend.objects.add_friend(from_user, to_user)
    #     except AlreadyExistsError as e:
    #         return JsonResponse({"error": str(e)})
    #     else:
    #         return JsonResponse({"msg": f"{body['to_user']} added as friend"})


    # @action(methods=["get"], detail=True)
    # def list_request(self, request, *args, **kwargs):
    #     friend_requests = Friend.objects.requests(request.user)
    #     print(friend_requests)
    #     # return HttpResponse(friend_requests)
    #     return JsonResponse({"requests": friend_requests})


    # @action(detail=True)
    # def list_friends(self, request, *args, **kwargs):
    #     pass


    # @action(detail=True)
    # def friends(self, request, *args, **kwargs):
    #     pass


    # @action(detail=True)
    # def friends(self, request, *args, **kwargs):
    #     pass


    # @action(detail=True)
    # def friends(self, request, *args, **kwargs):
    #     pass

