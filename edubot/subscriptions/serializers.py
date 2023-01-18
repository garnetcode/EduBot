"""Imports"""
from rest_framework.serializers import ModelSerializer

# pylint: disable = no-name-in-module
from subscriptions.models import (
    SubscriptionPackage,
    Subscription
)

class SubscriptionPackageSerializer(ModelSerializer):
    """SubscriptionPackageSerializer"""
    class Meta:
        """Meta definition for SubscriptionPackageSerializer."""
        model = SubscriptionPackage
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    """SubscriptionSerializer"""
    class Meta:
        """Meta definition for SubscriptionSerializer."""
        model = Subscription
        fields = "__all__"
