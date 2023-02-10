"""edubot URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from payments.views import PaymentsWebHook, PayPalWebhookView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webhook/", PaymentsWebHook.as_view(), name="webhook"),
    path("paypal/webhook/", PayPalWebhookView.as_view(), name="paypal_webhook"),
    path("api/", include("api.urls")),
    path("user/", include("users.urls")),
    path("dashboard/class/", include("tutorials.urls")),
    path("dashboard/courses/", include("courses.urls")),
    path("dashboard/package/", include("packages.urls")),
    path("dashboard/payments/", include("payments.urls")),
    path("dashboard/material/", include("material.urls")),
    path("dashboard/assignments/", include("assignments.urls")),
    path("dashboard/assessment/", include("quiz.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
