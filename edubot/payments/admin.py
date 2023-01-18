"""Admin for payments app."""
#pylint: disable = no-name-in-module
from django.contrib import admin
from payments.models import Payment, OutsourcingFees

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment Admin"""
    list_display = [f.name for f in Payment._meta.fields]

@admin.register(OutsourcingFees)
class OutsourcingFeesAdmin(admin.ModelAdmin):
    """OutsourcingFees Admin"""
    list_display = [f.name for f in OutsourcingFees._meta.fields]
