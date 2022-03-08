from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView

from . import serializers
from . import models

# Create your views here.
def ping(request):
    return JsonResponse({'success': True})


class ChatroomListAPIView(ListAPIView):
    queryset = models.Chatroom.objects.all()
    serializer_class = serializers.ChatroomSerializer


class UsersListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
