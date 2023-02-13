"""Serializers for the courses app."""
# pylint: disable = no-name-in-module
from rest_framework.serializers import ModelSerializer
from courses.models import Course
from tutorials.models import Conversation, Message
class CourseSerializer(ModelSerializer):
    """CourseSerializer"""
    class Meta:
        """Meta definition for CourseSerializer."""
        model = Course
        fields = (
            'id',
            'name',
            'description',
            'duration',

        )


class ConversationSerializer(ModelSerializer):
    """ConversationSerializer"""
    class Meta:
        """Meta definition for ConversationSerializer."""
        model = Conversation
        fields = (
            'id',
            'user',
            'course',
            'messages',
            'date_created',
        )

    def to_representation(self, instance):
        """Override the to_representation method."""
        representation = super().to_representation(instance)
        representation['messages'] = MessageSerializer(instance=instance.messages.all(), many=True).data
        return representation
    

class MessageSerializer(ModelSerializer):
    """MessageSerializer"""
    class Meta:
        """Meta definition for MessageSerializer."""
        model = Message
        fields = (
            'id',
            'sender',
            'content',
            'date_sent',
        )

    def to_representation(self, instance):
        """Override the to_representation method."""
        representation = super().to_representation(instance)
        representation['sender'] = instance.sender.first_name
        representation['sender_id'] = instance.sender.id
        return representation

