from django.urls import path

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('chatroom', views.ChatroomAPIView.as_view()),
    path('chatroom/<int:pk>/users', views.ChatroomUsersAPIView.as_view()),
    path('chatroom/<int:pk>/messages', views.MessagesAPIView.as_view()),
]