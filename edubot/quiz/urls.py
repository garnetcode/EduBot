"""URL Configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# pylint: disable = no-name-in-module
from quiz.views import (
    QuizViewset,
    QuestionViewset,
    ResultViewset
)

router = DefaultRouter()
router.register(r'quiz', QuizViewset, basename='quiz')
router.register(r'question', QuestionViewset, basename='question')
router.register(r'result', ResultViewset, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]