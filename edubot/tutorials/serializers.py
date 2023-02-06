"""Serializers for the tutorials app."""
from rest_framework import serializers

#pylint: disable=no-name-in-module
from tutorials.models import Tutorial, Lesson, CallRequest


class TutorialSerializer(serializers.ModelSerializer):
    """Serializer for the tutorial model."""
    class Meta:
        """Meta class for the tutorial serializer."""
        model = Tutorial
        fields = ('id', 'course','course', 'title', 'description', 'published')
    


    def to_representation(self, instance):
        """Override the to_representation method."""
        representation = super().to_representation(instance)
        representation['steps'] = StepSerializer(instance=instance.steps.all(), many=True).data
        representation['course_name'] = instance.course.name
        return representation
    
    def create(self, validated_data):
        """Override the create method."""
        validated_data['published_by'] = self.context['request'].user
        return super().create(validated_data)

class StepSerializer(serializers.ModelSerializer):
    """Serializer for the lesson model"""
    class Meta:
        """Meta class for the lesson model"""
        model = Lesson
        fields = ['id', 'title', 'instructions', 'tutorial_class', 'content_type', 'file']
        extra_kwargs = {
            'title': {'required': True},
            'instructions': {'required': True},
            'tutorial_class': {'required': True},
            'content_type': {'required': True},
            'file': {'required': False},
        }
    

    def validate(self, attrs):
        data =  super().validate(attrs)
        if data.get('content_type') in ['document', 'video', 'image', 'audio']:
            if not data.get('file'):
                raise serializers.ValidationError(
                    {"file":"This field is required"}
                )

        #pylint: disable=no-member
        if Lesson.lesson_exists(data.get('tutorial_class'), data.get('title')):
            raise serializers.ValidationError({"title":"This title already exists"})

        return data

    def to_representation(self, instance):
        """Override the to_representation method."""
        print("\n\nINSTANCE : ", instance)
        representation = super().to_representation(instance)
        print("REPRESENTATION : ", representation)
        return representation


class CallRequestSerializer(serializers.ModelSerializer):
    """Serializer for the call request model."""
    class Meta:
        """Meta class for the call request serializer."""
        model = CallRequest
        fields = ('id', 'requested_by', 'course', 'date_of_call', 'agenda', 'status', 'call_link')
        extra_kwargs = {
            'requested_by': {'required': False},
            'course': {'required': True},
            'date_of_call': {'required': True},
            'agenda': {'required': True},
        }

    def validate(self, attrs):
        data = super().validate(attrs)

        #pylint: disable=no-member
        if CallRequest.call_request_exists(data.get('requested_by'), data.get('course'), data.get('date_of_call')):
            raise serializers.ValidationError({"date_of_call":"This call request has already requested"})
        return data

    def create(self, validated_data):
        """Override the create method."""
        validated_data['requested_by'] = self.context['user']
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Override the to_representation method."""
        representation = super().to_representation(instance)
        representation['course_name'] = instance.course.name
        representation['requested_by_name'] = f"{instance.requested_by.first_name} {instance.requested_by.last_name}"
        representation['requested_by_phone'] = instance.requested_by.phone_number
        return representation

class LessonSerializer(serializers.ModelSerializer):
    """Serializer for the lesson model"""
    class Meta:
        """Meta class for the lesson model"""
        model = Lesson
        fields = '__all__'

    
