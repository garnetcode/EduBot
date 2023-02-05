"""Users views"""
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

#pylint: disable=no-name-in-module
from users.serializers import AuthTokenObtainPairSerializer, StaffSerializer


from .models import User


class AuthTokenObtainPairView(TokenObtainPairView):
    """Obtain token view"""
    serializer_class = AuthTokenObtainPairSerializer

class UserViewset(viewsets.ModelViewSet):
    """User ModelViewset"""
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StaffSerializer

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(role='STUDENT')
