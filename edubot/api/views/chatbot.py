"""Chatbot API views."""
# pylint: disable = import-error
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from services.action_picker import ActionPickerService


class CloudAPIWebhook(APIView):
    """
        Webhook
    """

    @staticmethod
    def post(request):
        """POST request handler for the webhook."""
        payload = dict(request.data)
        print("PAYLOAD >>>> ", payload)
        action_picker = ActionPickerService(payload=payload)
        action_picker.dispatch_action()
        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)


    def get(self, request):
        """GET request handler for the webhook."""
        form_data = request.query_params
        mode = form_data.get('hub.mode')
        token = form_data.get('hub.verify_token')
        challenge = form_data.get('hub.challenge')
        print(mode, token, challenge)
        return HttpResponse(challenge,200)
