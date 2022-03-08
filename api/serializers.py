from . import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chatroom
        fields = ('id', 'name', 'owner')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Messages
        fields = ('id', 'chatroom', 'user', 'text', 'date')
