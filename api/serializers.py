from . import models
from rest_framework import serializers


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chatroom
        fields = ('id', 'name', 'owner')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Messages
        fields = ('id', 'chatroom', 'user', 'text', 'date')
