"""Course Material Admin"""
from django.contrib import admin

#pylint: disable=no-name-in-module
from material.models import CourseMaterial

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    """Course Material Admin"""
    list_display = ["title", "content_type", "course"]
    list_filter = ["content_type", "course"]
    search_fields = ["title", "content_type", "course__title"]
    list_per_page = 20
