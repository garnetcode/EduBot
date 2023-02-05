"""Serializers for the assignments app"""
from rest_framework import serializers

#pylint: disable=no-name-in-module
from assignments.models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment Serializer"""
    class Meta:
        """Meta Class"""
        model = Assignment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    
    def to_representation(self, instance):
        """Override the to_representation method"""
        data = super().to_representation(instance)
        data["submitted_by_name"] = instance.submitted_by.get_full_name()
        # data["created_at"] = data["created_at"].strftime("%d %b %Y %H:%M:%S") if data["created_at"] else None
        # data["updated_at"] = data["updated_at"].strftime("%d %b %Y %H:%M:%S") if data["updated_at"] else None
        return data
