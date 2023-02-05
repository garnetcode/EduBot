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

    def validate(self, attrs):
        """Validate the data"""
        if attrs["content_type"] == "VIDEO" and not attrs["video_url"]:
            raise serializers.ValidationError("Video URL is required for video content type")
        return attrs
