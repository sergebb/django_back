from . import models
from rest_framework import serializers

class MessagesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = models.Messages
        fields = ('id', 'user', 'text', 'date')
        read_only_fields = ['id', 'user', 'date']


class ChatroomSerializer(serializers.ModelSerializer):
    last_message = MessagesSerializer(many=False, read_only=True)

    class Meta:
        model = models.Chatroom
        fields = ('id', 'last_message', 'name', 'owner')
        read_only_fields = ['last_message', 'owner']


class UserRoomsSerializer(serializers.ModelSerializer):
    joinedrooms = ChatroomSerializer

    class Meta:
        model = models.User
        fields = ('id', 'username', 'joinedrooms')


