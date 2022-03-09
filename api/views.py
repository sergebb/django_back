from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from djoser.serializers import UserSerializer

from . import serializers
from . import models

# Create your views here.
def ping(request):
    return JsonResponse({'success': True})


class ChatroomAPIView(generics.ListCreateAPIView):
    queryset = models.Chatroom.objects.all()
    serializer_class = serializers.ChatroomSerializer


class ChatroomUsersAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return models.Chatroom.objects.filter(pk=self.kwargs['pk']).all()

    def get(self, request, pk, format=None):
        user = request.user
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({'success': False, 'message': 'Bad chatroom'}, status=400)

        in_room = queryset[0].members.filter(id=user.id).count()
        if in_room == 0:
            return Response({'success': False, 'message': 'Not in chatroom'}, status=400)
        
        queryset = queryset[0].members.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        user = request.user
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({'success': False, 'message': 'Bad chatroom'}, status=400)

        in_room = queryset[0].members.filter(id=user.id).count()

        if in_room > 0:
            return Response({'success': False, 'message': 'Already in chatroom'}, status=400)
        
        tag = models.UserRooms(user=user, chatroom=queryset[0])
        tag.save()
        
        return Response({'success': True}, status=200)

    def delete(self, request, pk, format=None):
        user = request.user
        queryset = self.get_queryset()
        if len(queryset) == 0:
            return Response({'success': False, 'message': 'Bad chatroom'}, status=400)

        in_room = queryset[0].members.filter(id=user.id).count()

        if in_room == 0:
            return Response({'success': False, 'message': 'Not in chatroom'}, status=400)
        
        tag = models.UserRooms.objects.filter(user=user, chatroom=queryset[0])
        tag.delete()
        
        return Response({'success': True}, status=200)


class UsersListAPIView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
