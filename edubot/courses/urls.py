"""URLs for course app."""
from django.urls import path, include
from rest_framework import routers

#pylint: disable=no-name-in-module
from .views import CourseViewset

router = routers.DefaultRouter()
router.register(r'course', CourseViewset)

urlpatterns = [
    path('', include(router.urls)),
]