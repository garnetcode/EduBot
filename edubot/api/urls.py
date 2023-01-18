"""Urls for the API views."""
# pylint: disable = import-error

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from api.views.chatbot import CloudAPIWebhook


urlpatterns = [
    path('v1/webhook/', csrf_exempt(CloudAPIWebhook.as_view()), name='webhook'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)