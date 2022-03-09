from . import models
from rest_framework import serializers


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chatroom
        fields = ('id', 'name', 'owner')
        read_only_fields = ['owner']


class UserRoomsSerializer(serializers.ModelSerializer):
    joinedrooms = ChatroomSerializer

    class Meta:
        model = models.User
        fields = ('id', 'username', 'joinedrooms')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Messages
        fields = ('id', 'user', 'text', 'date')
        read_only_fields = ['id', 'user', 'date']
