"""Serializers for the assignments app"""
from datetime import datetime
from rest_framework import serializers

#pylint: disable=no-name-in-module
from assignments.models import Assignment, PendingWork

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
        data["created_at"] = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%d %b %Y %H:%M:%S")
        data["updated_at"] = datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%d %b %Y %H:%M:%S")
        return data


class PendingWorkSerializer(serializers.ModelSerializer):
    """Pending Work Serializer"""
    class Meta:
        """Meta Class"""
        model = PendingWork
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    
    def to_representation(self, instance):
        """Override the to_representation method"""
        data = super().to_representation(instance)
        data["submitted_assignments"] = AssignmentSerializer(instance.submitted_assignments, many=True).data
        data["uploaded_by_name"] = instance.uploaded_by.get_full_name() if instance.uploaded_by else None
        return data