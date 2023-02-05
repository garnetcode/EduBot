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

    
    def to_representation(self, instance):
        """Override the to_representation method."""
        representation = super().to_representation(instance)
        representation['user_name'] = f"{instance.user.first_name} {instance.user.last_name}"
        representation['course_name'] = instance.course.name
        representation['package'] = instance.package.name.capitalize() if instance.package else 'Not Specified'
        representation['payment_type'] = instance.get_payment_type_display()
        representation['method'] = instance.method.capitalize()
        return representation
