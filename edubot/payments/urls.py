"""Payments URL Configuration"""
from django.urls import path, include
from rest_framework import routers

from payments.views import PaymentViewSet

router = routers.DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
