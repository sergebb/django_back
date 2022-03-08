from django.urls import path
from .views import RegisterView
from rest_framework.authtoken import views


urlpatterns = [
    # path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.obtain_auth_token, name='auth_login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
