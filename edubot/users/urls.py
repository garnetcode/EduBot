"""Users URLs."""
from django.urls import path, include
from rest_framework import routers

#pylint: disable=no-name-in-module
from .views import AuthTokenObtainPairView, UserViewset

router = routers.DefaultRouter()
router.register(r'', UserViewset, basename='users')


urlpatterns = [
    path('login/', AuthTokenObtainPairView.as_view(), name='login'),
    path('', include(router.urls)),

]