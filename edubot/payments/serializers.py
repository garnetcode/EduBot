"""Serializers for payments app."""
from rest_framework import serializers

#Local imports
from payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    class Meta:
        """Meta class for PaymentSerializer."""
        model = Payment
        fields = '__all__'
