"""Admin for assignments app"""
#pylint: disable = no-name-in-module
from django.contrib import admin
from assignments.models import Assignment, PendingWork

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Assignment Admin"""
    list_display = [f.name for f in Assignment._meta.fields]

@admin.register(PendingWork)
class PendingWorkAdmin(admin.ModelAdmin):
    """AssignmentSubmission Admin"""
    list_display = [f.name for f in PendingWork._meta.fields]
