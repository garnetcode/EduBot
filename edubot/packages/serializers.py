"""Serializers for the Package model"""
# Description: Serializers for the Package model
from rest_framework import serializers
from .models import Package

class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package model"""
    class Meta:
        """Meta class for PackageSerializer"""
        model = Package
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'description': {'required': False}
        }


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        permissions = [
            'Curated Content',
            'Curated Content + Whatsapp Calls',
            'Curated Content + Whatsapp Calls + Zoom Calls',
            'Curated Content + Whatsapp Calls + Zoom Calls + Live Classes'
        ]
        data['access_permissions'] =  permissions[int(instance.access_permissions) - 1]
        return data
