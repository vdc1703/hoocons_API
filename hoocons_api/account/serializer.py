# This file use to return the json format

from account.models import Account, RelationShip, FriendshipRequest
from rest_framework import serializers
from location.serializers import LocationSerializer
from django.db.models import Q

from utils import app_constant

# use for return in Jason, __all__ mean all columns in table

class AccountSerializer(serializers.ModelSerializer):
    # call function get_username_from_pk
    username = serializers.SerializerMethodField("get_username_from_pk")

    # call function check_if_self
    is_self = serializers.SerializerMethodField("check_is_self")

    # # call function check_if_friend
    # is_friend = serializers.SerializerMethodField("check_is_friend")
    #
    # call function get_location_by_point
    location = serializers.SerializerMethodField("get_location_by_point")

    # # call function check_is_sent_friend_quest
    # friend_requested = serializers.SerializerMethodField("check_is_sent_friend_request")
    #

    def get_username_from_pk(self, data):
        # data = Account object
        # data.user = username
        user = data.user
        return user.username

    # This use to check who is viewing this user, is self or from other
	# this function if for User_Views.py, to allow user view profile
    def check_is_self(self, data):
        user_info = self.context.get('request').user
        if data.user == user_info:
             return True
        else:
             return False

    # # Function use to check if user sent friend request
    # def check_is_sent_friend_request(self, userinfo):
    #     # get
    #     user_info = self.context.get('request').user.userinfo
    #     print('test', user_info)
    #
    #     try:
    #         # get info from FriendshipRequest object
    #         FriendshipRequest.objects.get(sender=user_info, receiver=userinfo)
    #         return True
    #     except FriendshipRequest.DoesNotExist:
    #         return False
    #

    #
    # def check_is_friend(self, userinfo):
    #     user_info = self.context.get('request').user.userinfo
    #     try:
    #         RelationShip.objects.get(Q(from_user=user_info, to_user=userinfo) |
    #                                  Q(from_user=userinfo, to_user=user_info),
    #                                  status=app_constant.R_FRIEND)
    #         return True
    #     except RelationShip.DoesNotExist:
    #         return False
    #
    def get_location_by_point(self, userinfo):
        return LocationSerializer(userinfo.location, many=False).data


    class Meta:
        model = Account
        fields = "__all__"
        extra_fields = ['username', 'is_self', 'location']
