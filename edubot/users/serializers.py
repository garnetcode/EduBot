"""Seiralizers for the users app."""
# pylint: disable = no-name-in-module
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import User

class UserSerializer(ModelSerializer):
    """UserSerializer"""
    class Meta:
        """Meta definition for UserSerializer."""
        model = User
        fields = "__all__"

    def validate(self, attrs):
        """Validate the user data"""
        data = super().validate(attrs)
        if not data.get('first_name'):
            raise serializers.ValidationError("First name is required")
        if not data.get('last_name'):
            raise serializers.ValidationError("What is your last name?")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required")
        if not data.get('email'):
            raise serializers.ValidationError("What is your email address?")
        if not data.get('sex'):
            raise serializers.ValidationError("What is your sex?")
        return data
