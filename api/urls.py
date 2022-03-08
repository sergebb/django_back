from django.urls import path

from . import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('users', views.UsersListAPIView.as_view()),
    path('chatroom', views.ChatroomAPIView.as_view()),
    path('chatroom/<int:pk>/users', views.ChatroomUsersAPIView.as_view()),
]