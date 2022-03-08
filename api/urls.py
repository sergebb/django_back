from django.urls import path

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('users', views.UsersListAPIView.as_view(), name='api_users'),
    path('chatroom', views.ChatroomListAPIView.as_view(), name='api_chatrooms'),
]