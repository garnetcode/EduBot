"""Chatbot API views."""
# pylint: disable = import-error
import json
import requests
from django.core.cache import cache
from decouple import config
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from services.action_picker import ActionPickerService

def send_response(response):
    """Send the response."""
    url = f"https://graph.facebook.com/v15.0/{config('Phone_Number_ID')}/messages"
    response = requests.post(
        url=url,
        data=response,
        headers={'Authorization': f'Bearer {config("CLOUD_API_TOKEN")}'}
    )
    return response


class CloudAPIWebhook(APIView):
    """
        Webhook
    """

    @staticmethod
    def post(request):
        """POST request handler for the webhook."""
        payload = dict(request.data)
        # print("PAYLOAD >>>> ", payload)
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


class Navigation(APIView):
    """
        Webhook
    """

    @staticmethod
    def post(request):
        """POST request handler for the webhook."""
        payload = dict(request.data)

        # all items in cache
        print("NAVIGATION >>>> ", payload, cache.get(f"{payload.get('recipient_id')}_nav"))
        record = cache.get(f"{payload.get('recipient_id')}_nav")
        if record:
            if payload.get('status') == "read" and record.get('type') in ["nav"]:
                # print("READ >>>> ", record)
                messages = {
                    "document": "Use buttons for navigation",
                    "audio": "Use buttons for navigation",
                    "video": "Use the buttons below for navigation",
                    "image": "Use the buttons below for navigation",
                }
                response_data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": payload.get('recipient_id'),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": record.get('caption') if record.get('response_type') in ["audio"] else messages.get(record.get('response_type'))
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "tutorial_prev",
                                        "title": "🔙 Previous"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "tutorial_next",
                                        "title": "🔜 Forward "
                                    }
                                }
                            ]
                        }
                    }
                }
                if record.get('is_first_step'):
                    response_data["interactive"]["action"]["buttons"].pop(0)
                else:
                    if record.get('is_last_step'):
                        response_data["interactive"]["action"]["buttons"][1]['reply']['title'] = "🏁 Finish"
                interactive = json.dumps(response_data.pop("interactive"))
                response_data["interactive"] = interactive
                send_response(response_data)
                cache.delete(f"{payload.get('recipient_id')}_nav")
            elif payload.get('status') == "read" and record.get('type') in ["quiz"]:
                print("READ >>>> ", record)
                response_data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": payload.get('recipient_id'),
                    "type": "interactive",
                    "interactive": json.dumps({
                        "type": "list",
                        "body": {
                            "text": " Select the most appropriate answer "
                        },
                        "action": {
                            "button": "Select Choices",
                            "sections": [
                                {
                                    "title": "Select Choice",
                                    "rows": [
                                        {
                                            "id": item,
                                            "title": item,
                                        } for item in ["A", "B", "C", "D"]
                                    ]
                                }
                            ]
                        }
                    })
                }
                resp = send_response(response_data)
                print("RESPONSE >>>> ", resp.json())
                cache.delete(f"{payload.get('recipient_id')}_nav")

        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

                        