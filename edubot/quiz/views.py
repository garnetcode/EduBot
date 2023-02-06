"""Views for the quiz app."""
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

#pylint: disable=no-name-in-module
from users.permissions import IsStaff



#Local imports
from quiz.serializers import QuizSerializer, QuestionSerializer, ResultSerializer
from quiz.models import Quiz, Question, Result

class QuizViewset(viewsets.ModelViewSet):
    """Quiz viewset."""
    serializer_class = QuizSerializer
    #pylint: disable=no-member
    queryset = Quiz.objects.all()
    permission_classes = [IsStaff]

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Returns all questions for a quiz."""
        quiz = self.get_object()
        questions = quiz.get_questions()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Returns all results for a quiz."""
        quiz = self.get_object()
        results = quiz.get_results()
        serializer = ResultSerializer(results, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=['post'], url_path='add_question')
    def add_question(self, request, pk=None):
        """Adds a question to a quiz."""
        quiz = self.get_object()
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            quiz.questions.add(question)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False)
    
    @action(detail=True, methods=['get'], url_path='course')
    def filter_by_course(self, request, pk=None):
        """Returns all quizzes for a course."""
        queryset = Quiz.objects.filter(course=pk)
        serializer = QuizSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)



class QuestionViewset(viewsets.ModelViewSet):
    """Question viewset."""
    serializer_class = QuestionSerializer
    #pylint: disable=no-member
    queryset = Question.objects.all()
    permission_classes = [IsStaff]



class ResultViewset(viewsets.ModelViewSet):
    """Result viewset."""
    serializer_class = ResultSerializer
    #pylint: disable=no-member
    queryset = Result.objects.all()
    permission_classes = [IsStaff]

    @action(detail=True, methods=['get'], url_path='user')
    def filter_by_user(self, request, pk=None):
        """Returns all results for a user."""
        queryset = Result.objects.filter(user=pk)
        serializer = ResultSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)