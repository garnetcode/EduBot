"""Subscriptions Admin"""
from django.contrib import admin

# pylint: disable = no-name-in-module
from subscriptions.models import (
    Subscription
)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Subscription Admin"""
    list_display = [f.name for f in Subscription._meta.fields]
