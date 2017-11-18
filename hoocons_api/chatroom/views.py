from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import Account
from chatroom.models import ChatRoom
from chatroom.serializers import ChatRoomSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 20
    parser_classes = (JSONParser,)

    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def list(self, request, *args, **kwargs):
        try:
            current_user = request.user
            if current_user is None:
                return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            elif current_user.is_active is False:
                return Response({"message": "user is inactive or banned"}, status=status.HTTP_423_LOCKED)
        except User.DoesNotExist:
            return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # Update user action
        user_info = get_object_or_404(Account, pk=current_user)
        user_info.last_action_at = now()
        user_info.save()

        try:
            chatrooms = user_info.chatroom_set.distinct()
            return Response(ChatRoomSerializer(chatrooms, many=True, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        except ChatRoom.DoesNotExist:
            return Response([], status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        try:
            current_user = request.user
            if current_user is None:
                return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            elif current_user.is_active is False:
                return Response({"message": "user is inactive or banned"}, status=status.HTTP_423_LOCKED)
        except User.DoesNotExist:
            return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Update user action
        user_info = get_object_or_404(Account, pk=current_user)
        user_info.last_action_at = now()
        user_info.save()

        if request.data is not None:
            try:
                users = request.data["users"]
                uid = request.data["uid"]

                if len(users) < 2:
                    return Response(
                        {
                            "message": "cannot create chatroom"
                        }, status=status.HTTP_206_PARTIAL_CONTENT
                    )

                list_users = []
                for user in users:
                    try:
                        user_obj = Account.objects.get(user_id=int(user)).user_id
                        list_users.append(user_obj)
                    except Account.DoesNotExist:
                        return Response({"message": "user not found"}, status.HTTP_404_NOT_FOUND)

                # Now try to look for duplicate
                try:
                    chatrooms = ChatRoom.objects.filter(users__in=list_users).distinct()
                    for chatroom in chatrooms:
                        ids = chatroom.users.values_list('user_id', flat=True)
                        print(ids)
                        if set(list_users) == set(ids):
                            return Response({"message": "chatroom already created"}, status=status.HTTP_201_CREATED)
                except ChatRoom.DoesNotExist:
                    pass

                chatroom = ChatRoom.objects.create(uid=uid)
                for user in list_users:
                    chatroom.active_with.add(user)
                    chatroom.users.add(user)

                return Response({"message": "success"}, status=status.HTTP_200_OK)
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pass

    def update(self, request, pk=None, *args, **kwargs):
        pass

    def partial_update(self, request, pk=None, *args, **kwargs):
        pass

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            current_user = request.user
            if current_user is None:
                return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
            elif current_user.is_active is False:
                return Response({"message": "user is inactive or banned"}, status=status.HTTP_423_LOCKED)
        except User.DoesNotExist:
            return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # Update user action
        user_info = get_object_or_404(Account, pk=current_user)
        user_info.last_action_at = now()
        user_info.save()

        # Getting chatroom information
        chatroom = get_object_or_404(ChatRoom, id=pk)
        if user_info in chatroom.active_with:
            chatroom.active_with.remove(user_info)
            if chatroom.active_with.count() == 0:
                chatroom.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "not in that chat room"}, status=status.HTTP_204_NO_CONTENT)
