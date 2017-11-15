# This file use to return the json format

from account.models import Account, RelationShip, FriendshipRequest
from rest_framework import serializers
from location.serializers import LocationSerializer
from django.db.models import Q

from utils import app_constant

# use for return in Jason, __all__ mean all columns in table

class AccountSerializer(serializers.ModelSerializer):
	# return username
    username = serializers.SerializerMethodField("get_username_from_pk")
	
    is_self = serializers.SerializerMethodField("check_is_self")
    is_friend = serializers.SerializerMethodField("check_is_friend")
    location = serializers.SerializerMethodField("get_location_by_point")
    friend_requested = serializers.SerializerMethodField("check_is_sent_friend_request")

    def check_is_sent_friend_request(self, userinfo):
        user_info = self.context.get('request').user.userinfo
        try:
            FriendshipRequest.objects.get(sender=user_info, receiver=userinfo)
            return True
        except FriendshipRequest.DoesNotExist:
            return False


    def check_is_self(self, userinfo):
        user_info = self.context.get('request').user.userinfo
        if userinfo == user_info:
            return True
        else:
            return False

    def check_is_friend(self, userinfo):
        user_info = self.context.get('request').user.userinfo
        try:
            RelationShip.objects.get(Q(from_user=user_info, to_user=userinfo) |
                                     Q(from_user=userinfo, to_user=user_info),
                                     status=app_constant.R_FRIEND)
            return True
        except RelationShip.DoesNotExist:
            return False

    def get_location_by_point(self, userinfo):
        return LocationSerializer(userinfo.location, many=False).data

    def get_username_from_pk(self, userinfo):
        user = userinfo.user
        return user.username

    class Meta:
        model = Account
        fields = "__all__"
        extra_fields = ['username', 'is_self', 'is_friend', 'friend_requested']







class FriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_sender_info")

    def get_sender_info(self, friendshiprequest):
        return SimpleUserInfoSerializer(friendshiprequest.sender, many=False,
                                        context={"request": self.context.get('request')}).data

    class Meta:
        model = FriendshipRequest
        fields = ("id", "user", "request_made_at", "message", "found_user_from")








class RelationshipSerializer(serializers.ModelSerializer):
    with_user = serializers.SerializerMethodField("get_rel_with_user")

    def get_rel_with_user(self, relationship):
        user_info = self.context.get('request').user.userinfo
        if relationship.from_user == user_info:
            return SimpleUserInfoSerializer(relationship.to_user, many=False,
                                            context={"request": self.context.get('request')}).data
        else:
            return SimpleUserInfoSerializer(relationship.from_user, many=False,
                                            context={"request": self.context.get('request')}).data

    class Meta:
        model = RelationShip
        fields = ("id", "with_user", "rel_made_at", "status")
