from rest_framework import generics

from api.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(RegisterView, self).get_permissions()
