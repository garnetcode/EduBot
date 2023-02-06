"""Quiz serializers."""
from rest_framework import serializers

# pylint: disable = no-name-in-module
from quiz.models import Quiz, Question, Result

class QuizSerializer(serializers.ModelSerializer):
    """Quiz serializer."""
    questions = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""
        model = Quiz
        fields = '__all__'

    def get_questions(self, obj):
        """Returns all questions for a quiz."""
        return QuestionSerializer(obj.get_questions(), many=True).data

    def get_results(self, obj):
        """Returns all results for a quiz."""
        return ResultSerializer(obj.get_results(), many=True).data


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""
    class Meta:
        """Meta class."""
        model = Question
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    """Result serializer."""
    class Meta:
        """Meta class."""
        model = Result
        fields = '__all__'
