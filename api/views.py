from django.http import JsonResponse, Http404
from django.db.models.functions import Now
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg import openapi
from djoser.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema, no_body

from . import serializers
from . import models

# Create your views here.


def ping(request):
    return JsonResponse({'success': True})


class ChatroomAPIView(generics.ListCreateAPIView):
    queryset = models.Chatroom.objects.all()
    serializer_class = serializers.ChatroomSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ChatroomUsersAPIView(generics.GenericAPIView):
    queryset = models.Chatroom.objects.all()
    serializer_class = serializers.ChatroomSerializer

    def get_object(self, pk):
        try:
            return models.Chatroom.objects.get(pk=pk)
        except models.Chatroom.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="List users in a chatroom",
                         responses={
                             404: 'Chatroom not found',
                             403: 'Not in a chatroom',
                             200: UserSerializer(many=True)
                         })
    def get(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_object(pk)

        in_room = chatroom.members.filter(id=user.id).count()
        if in_room == 0:
            return Response({'message': 'Not in a chatroom'}, status=status.HTTP_403_FORBIDDEN)

        joined_users = chatroom.members.all()
        serializer = UserSerializer(joined_users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Join the chatroom",
                         request_body=no_body,
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


class MessagesAPIView(generics.GenericAPIView):
    queryset = models.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer

    def get_chatroom(self):
        return models.Chatroom.objects.filter(pk=self.kwargs['pk']).first()


    @swagger_auto_schema(
        operation_description="Get list of messages",
        manual_parameters=[
            openapi.Parameter('lastMessage', openapi.IN_QUERY,
                              description='id of last recieved message', type=openapi.TYPE_INTEGER),
        ],
        responses={
            404: 'Chatroom not found',
            403: 'Not in a chatroom',
            200: serializers.MessagesSerializer
        })
    def get(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_chatroom()

        in_room = chatroom.members.filter(id=user.id).count()
        if in_room == 0:
            return Response({'message': 'Not in a chatroom'}, status=status.HTTP_403_FORBIDDEN)

        last_message_id = request.query_params.get('lastMessage')
        last_message = models.Messages.objects.filter(
            pk=last_message_id).first()

        messages = models.Messages.objects.filter(chatroom=chatroom)
        if last_message:
            messages = messages.filter(date__gt=last_message.date)

        serializer = serializers.MessagesSerializer(messages, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Post message",
        request_body=serializers.MessagesSerializer,
        responses={
            404: 'Chatroom not found',
            403: 'Not in a chatroom',
            400: 'Bad request',
            200: serializers.MessagesSerializer
        })
    def post(self, request, pk, format=None):
        user = request.user
        chatroom = self.get_chatroom()

        in_room = chatroom.members.filter(id=user.id).count()
        if in_room == 0:
            return Response({'message': 'Not in a chatroom'}, status=status.HTTP_403_FORBIDDEN)

        new_message = models.Messages(chatroom=chatroom, user=user, date=Now())
        serializer = serializers.MessagesSerializer(new_message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
