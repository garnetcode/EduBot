"""Material Serializers"""
from rest_framework import serializers

#pylint: disable=no-name-in-module
from material.models import CourseMaterial

class MaterialSerializer(serializers.ModelSerializer):
    """Material Serializer"""
    class Meta:
        """Meta Class"""
        model = CourseMaterial
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
