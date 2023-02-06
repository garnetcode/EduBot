"""URL Configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

#pylint: disable=no-name-in-module
from assignments.views import AssignmentViewset, PendingWorkViewset

router = DefaultRouter()

router.register(r"uploaded_work", PendingWorkViewset, basename="pending_work")
router.register(r"", AssignmentViewset, basename="assignment")

urlpatterns = [
    path("", include(router.urls)),
]