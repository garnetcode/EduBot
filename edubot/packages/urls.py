"""Urls for the edubot packages app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

#pylint: disable=no-name-in-module
from packages.views import PackageViewSet

router = DefaultRouter()
router.register(r'', PackageViewSet, basename='packages')

urlpatterns = [
    path('', include(router.urls)),
]
    