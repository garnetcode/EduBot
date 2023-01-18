"""Admin for courses app."""
from django.contrib import admin

# pylint: disable = no-name-in-module
from courses.models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course Admin"""
    list_display = [f.name for f in Course._meta.fields]
