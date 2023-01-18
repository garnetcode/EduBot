"""Serializers for the courses app."""
# pylint: disable = no-name-in-module
from rest_framework.serializers import ModelSerializer
from courses.models import Course

class CourseSerializer(ModelSerializer):
    """CourseSerializer"""
    class Meta:
        """Meta definition for CourseSerializer."""
        model = Course
        fields = "__all__"
