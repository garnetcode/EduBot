"""URL Configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

#pylint: disable=no-name-in-module
from material.views import MaterialViewset

router = DefaultRouter()

router.register(r"", MaterialViewset, basename="material")

urlpatterns = [
    path("", include(router.urls)),
]
