# use for deny or accept friend request

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import RelationShip, FriendshipRequest

from account.serializer import FriendRequestSerializer

#from activity.models import Activity

from utils import app_constant
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class FriendRequestView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    pagination_class = PageNumberPagination
    parser_classes = (JSONParser,)

    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendRequestSerializer

    # GET API for
    # View who request friend
    def list(self, request, *args, **kwargs):
        _current_user = request.user.account
        _current_user.last_action_at = now()
        _current_user.save()

        # cache model FriendshipRequest object
        requests = FriendshipRequest.objects.filter(Q(receiver=_current_user)).order_by("-request_made_at")

        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST
    def create(self, request, *args, **kwargs):
        return Response({"message": "currently not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



    # 	Accept friend request
    # def update(self, request, pk=None, *args, **kwargs):
    #     _current_user = request.user.userinfo
    #     _current_user.last_action_at = now()
    #     _current_user.save()
    #
    #     req = get_object_or_404(FriendshipRequest, pk=pk)
    #     # Accept friend request
    #     RelationShip.objects.create(from_user=_current_user, to_user=req.sender,
    #                                 status=app_constant.R_FRIEND)
    #     # Create activity object for two users
    #     Activity.objects.create(actor=_current_user, privacy=app_constant.privacy_private,
    #                             tag=app_constant.action_making_friend, target=req.sender)
    #
    #     Activity.objects.create(actor=req.sender, privacy=app_constant.privacy_private,
    #                             tag=app_constant.action_making_friend, target=_current_user)
    #     req.delete()
    #     return Response({"message": "success"}, status=status.HTTP_200_OK)


    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response({"message": "patch currently not supported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Denied/delete the friend request
    def destroy(self, request, pk=None, *args, **kwargs):
        _current_user = request.user.account
        _current_user.last_action_at = now()
        _current_user.save()
        req = get_object_or_404(FriendshipRequest, pk=pk)
        # Deny friend request
        req.delete()
        return Response({"message": "success"}, status=status.HTTP_200_OK)