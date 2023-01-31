"""Tutorials admin."""
#pylint: disable=import-error
from django.contrib import admin
#pylint: disable=no-name-in-module
from tutorials.models import Lesson, Tutorial, CallRequest

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson admin."""
    #pylint: disable=protected-access
    #pylint: disable=no-member
    list_display = [i.name for i in Lesson._meta.fields]
    list_filter = ['tutorial', 'title', 'instructions']
    search_fields = ['title', 'instructions']

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    """Tutorial Admin"""
    #pylint: disable=protected-access
    #pylint: disable=no-member
    list_display = [i.name for i in Tutorial._meta.fields]
    list_filter = ['course', 'title', 'description']

@admin.register(CallRequest)
class CallRequestAdmin(admin.ModelAdmin):
    """Call Request Admin"""
    #pylint: disable=protected-access
    #pylint: disable=no-member
    list_display = [i.name for i in CallRequest._meta.fields]
    list_filter = ['requested_by', 'course', 'date_of_call']
    search_fields = ['requested_by', 'course', 'date_of_call']


# Path: edubot/tutorials/models.py
