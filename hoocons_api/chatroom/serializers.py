from rest_framework import serializers

from account.serializer import SimpleUserInfoSerializer
from chatroom.models import ChatRoom


class ChatRoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField("get_users_list")

    def get_users_list(self, chatroom):
        request = self.context.get('request')
        return SimpleUserInfoSerializer(chatroom.users,
                                        many=True, context={"request": request}).data

    class Meta:
        model = ChatRoom
        fields = ('id', 'users', 'room_type', 'uid')