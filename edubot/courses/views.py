"""Courses Views"""
from rest_framework import viewsets

#pylint: disable=no-name-in-module
from users.permissions import IsStaff

#Local imports
from .serializers import CourseSerializer
from .models import Course


class CourseViewset(viewsets.ModelViewSet):
    """Course Viewset"""
    #pylint: disable=no-member
    queryset = Course.objects.all().exclude(code="COUT")
    permission_classes = (IsStaff, )
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "TUTOR":
            queryset = queryset.filter(instructors=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Override the create method."""
        serializer.save(instructors=[self.request.user])
        return super().perform_create(serializer)
