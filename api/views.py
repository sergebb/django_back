from django.http import JsonResponse, Http404
from rest_framework import generics, status
from rest_framework.response import Response
from djoser.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema

from . import serializers
from . import models

# Create your views here.
def ping(request):
    return JsonResponse({'success': True})


class ChatroomAPIView(generics.ListCreateAPIView):
    queryset = models.Chatroom.objects.all()
    serializer_class = serializers.ChatroomSerializer


class ChatroomUsersAPIView(generics.GenericAPIView):
    def get_object(self, pk):
        try:
            return models.Chatroom.objects.get(pk=pk)
        except models.Chatroom.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="List users in a chatroom", 
                         responses={
                             404: 'Chatroom not found',
                             400: 'Not in a chatroom',
                             200: UserSerializer
                         })
    def get(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_object(pk)

        in_room = chatroom.members.filter(id=user.id).count()
        if in_room == 0:
            return Response({'message': 'Not in a chatroom'}, status=status.HTTP_400_BAD_REQUEST)
        
        joined_users = chatroom.members.all()
        serializer = UserSerializer(joined_users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Join the chatroom", 
                         responses={
                            404: 'Chatroom not found',
                            400: 'Already in a chatroom',
                            200: serializers.UserRoomsSerializer
                         })
    def post(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_object(pk)

        in_room = chatroom.members.filter(id=user.id).count()
        if in_room > 0:
            return Response({'message': 'Already in a chatroom'}, status=status.HTTP_400_BAD_REQUEST)
        
        tag = models.UserRooms(user=user, chatroom=chatroom)
        tag.save()

        serializer = serializers.UserRoomsSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Leave the chatroom", 
                         responses={
                            404: 'chatroom not found'
                         })
    def delete(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_object(pk)

        tag = models.UserRooms.objects.filter(user=user, chatroom=chatroom)
        tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
