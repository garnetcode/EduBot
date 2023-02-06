from django.contrib import admin

# pylint: disable = no-name-in-module
from quiz.models import Quiz, Question, Result

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Quiz Admin"""
    #pylint: disable=no-member
    #pylint: disable=protected-access
    list_display = [f.name for f in Quiz._meta.fields]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question Admin"""
    #pylint: disable=no-member
    #pylint: disable=protected-access
    list_display = [f.name for f in Question._meta.fields]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Result Admin"""
    #pylint: disable=no-member
    #pylint: disable=protected-access
    list_display = [f.name for f in Result._meta.fields]
