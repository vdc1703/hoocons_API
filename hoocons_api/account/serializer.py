# Serializer use to return JSON format from given information

from account.models import Account, RelationShip, FriendshipRequest
from rest_framework import serializers
from location.serializers import LocationSerializer
from django.db.models import Q

from utils import app_constant


#----------------------------------------------------
# Account return JSON
#----------------------------------------------------
class AccountSerializer(serializers.ModelSerializer):
    # call function get_username_from_pk
    username = serializers.SerializerMethodField("get_username_from_pk")

    # call function check_if_self
    is_self = serializers.SerializerMethodField("check_is_self")

    # call function check_if_friend
    is_friend = serializers.SerializerMethodField("check_is_friend")

    # call function get_location_by_point
    location = serializers.SerializerMethodField("get_location_by_point")

    # # call function check_is_sent_friend_quest
    friend_requested = serializers.SerializerMethodField("check_is_sent_friend_request")


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

    # Function use to check if user sent friend request
    def check_is_sent_friend_request(self, data):
        # get request object from user ID
        user_info = self.context.get('request').user.account
        try:
            # get info from FriendshipRequest object
            FriendshipRequest.objects.get(sender=user_info, receiver=data)
            return True
        except FriendshipRequest.DoesNotExist:
            return False

    # this function based on relationship object to check if the viewer is friend or not
    def check_is_friend(self, data):
        user_info = self.context.get('request').user.account
        try:
            RelationShip.objects.get(Q(from_user=user_info, to_user=data) |
                                     Q(from_user=data, to_user=user_info),
                                     status=app_constant.R_FRIEND)
            return True
        except RelationShip.DoesNotExist:
            return False

    # get location from location Object
    def get_location_by_point(self, info):
        return LocationSerializer(info.location, many=False).data


    class Meta:
        model = Account
        fields = "__all__"
        extra_fields = ['username', 'is_self', 'is_friend', 'friend_requested']
#----------------------------------------------------
# End Account JSON
#----------------------------------------------------


#----------------------------------------------------
# Simple User information JSON
#----------------------------------------------------
class SimpleUserInfoSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField("check_is_friend")
    friend_requested = serializers.SerializerMethodField("check_is_sent_friend_request")
    location = serializers.SerializerMethodField("get_location_json")

    def get_location_json(self, _info):
        return LocationSerializer(_info.location, many=False).data

    def check_is_sent_friend_request(self, user):
        user_info = self.context.get('request').user.account
        try:
            FriendshipRequest.objects.get(sender=user_info, receiver=user)
            return True
        except FriendshipRequest.DoesNotExist:
            return False

    # this function based on relationship object to check if the viewer is friend or not
    def check_is_friend(self, data):
        user_info = self.context.get('request').user.account
        try:
            RelationShip.objects.get(Q(from_user=user_info, to_user=data) |
                                     Q(from_user=data, to_user=user_info),
                                     status=app_constant.R_FRIEND)
            return True
        except RelationShip.DoesNotExist:
            return False


    class Meta:
        model = Account
        fields = ("user", "display_name", "nickname", "avatar_url", "wallpaper_url", "last_action",
"location", "is_sharing_location", 'is_friend', 'friend_requested')
#----------------------------------------------------
# END Simple User information JSON
#----------------------------------------------------

#----------------------------------------------------
# Friend Request return JSON
#----------------------------------------------------
class FriendRequestSerializer(serializers.ModelSerializer):
        user = serializers.SerializerMethodField("get_sender_info")

        def get_sender_info(self, friendshiprequest):
            return SimpleUserInfoSerializer(friendshiprequest.sender, many=False,
                                                context={"request": self.context.get('request')}).data

        class Meta:
            model = FriendshipRequest
            fields = ("id", "user", "request_made_at", "message", "found_user_from")

#----------------------------------------------------
# Simple User information Object
#----------------------------------------------------