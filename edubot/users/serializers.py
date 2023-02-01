"""Seiralizers for the users app."""
# pylint: disable = no-name-in-module
# pylint: disable = import-error
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

from users.models import User

#pylint: disable = abstract-method
class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    """AuthTokenObtainPairSerializer"""
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = StaffSerializer(self.user).data
        return data

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

class StaffSerializer(ModelSerializer):
    """UserSerializer"""
    class Meta:
        """Meta definition for UserSerializer."""
        model = User
        fields = "__all__"
        extra_kwargs = {
            'username': {'required': False},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'role': {'required': True},
            'is_active': {'required': True},
            'role': {'required': True},
        }

    
    def validate(self, attrs):
        """Validate user data"""
        data = super().validate(attrs)
        data['username'] = data.get('email')
        data['is_staff'] = True
        data['password'] = make_password(data.get("password"))
        return data

    def to_representation(self, instance):
        """Convert the user object to a dictionary"""
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "phone_number": instance.phone_number,
            "role": instance.role,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
        }
