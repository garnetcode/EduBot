"""edubot URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from payments.views import PaymentsWebHook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("webhook/", PaymentsWebHook.as_view(), name="webhook"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
