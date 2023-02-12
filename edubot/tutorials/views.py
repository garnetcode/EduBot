"""Views for the tutorials app."""
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework import viewsets
from django.http import JsonResponse
from decouple import config
import requests

#Local imports.
#pylint: disable=no-name-in-module
#pylint: disable=import-error
from tutorials.models import (
    Tutorial,
    Lesson,
    CallRequest
)
from tutorials.serializers import (
    TutorialSerializer,
    StepSerializer,
    LessonSerializer,
    CallRequestSerializer,
    
)

#pylint: disable=no-name-in-module
from users.permissions import IsStaff
from users.models import User



class TutorialViewSet(viewsets.ModelViewSet):
    """Viewset for the Tutorial model."""

    #pylint: disable=no-member
    queryset = Tutorial.objects.all()
    permission_classes = (IsStaff,)
    renderer_classes = [JSONRenderer]
    serializer_class = TutorialSerializer

    def get_queryset(self):
        """Get queryset for the Tutorial model."""
        #pylint: disable=no-member
        if self.request.user.role == 'ADMIN':
            return Tutorial.objects.all()
        return Tutorial.objects.filter(published_by=self.request.user)

    @action(detail=False, methods=['post'], url_path='add_step')
    def steps(self, request):
        """Add a step to a tutorial."""
        serializer = StepSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serializer.validated_data['tutorial_class'].steps.add(serializer.instance)
            serializer.validated_data['tutorial_class'].save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    #pylint: disable=unused-argument
    @action(detail=False, methods=['get'], url_path='remove_step/(?P<tutorial_id>[0-9a-f-]+)/(?P<step_id>[0-9]+)')
    def remove_step(self, request, tutorial_id, step_id):
        """Remove a step from a tutorial."""
        #pylint: disable=no-member
        tutorial = Tutorial.objects.filter(id=tutorial_id).first()
        #pylint: disable=expression-not-assigned
        tutorial.steps.remove(step_id) if tutorial and tutorial.steps.filter(id=step_id).exists() else None
        return JsonResponse(
            {"message":"Step removed successfully" if tutorial else "Tutorial not found"},
            status=200 if tutorial else 404
            )


class CallRequestViewSet(viewsets.ModelViewSet):
    """Viewset for the CallRequest model."""

    #pylint: disable=no-member
    queryset = CallRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = [JSONRenderer]
    serializer_class = CallRequestSerializer

    def get_queryset(self):
        """Get queryset for the CallRequest model."""
        #pylint: disable=no-member
        if self.request.user.role == 'ADMIN':
            return CallRequest.objects.all()
        return CallRequest.objects.filter(course__instructors__in=self.request.user)

    def update(self, request, *args, **kwargs):
        data =  super().update(request, *args, **kwargs)
        if data.status_code == 200:
            data.data['message'] = "Call request updated successfully"
            requested_by = User.objects.filter(id=data.data['requested_by']).first()
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": requested_by.phone_number,
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": f"Your call request with agenda *{data.data['agenda']}* has been updated with status {data.data['status'].title()}\n\n{'Call Link : ' + data.data['call_link']}"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": f"decline_call_request_{data.data['id']}",
                                    "title": "Decline"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": f"accept_call_request_{data.data['id']}",
                                    "title": "Accept"
                                }
                            }
                        ]
                    }
                })
            }
            url = f"https://graph.facebook.com/v15.0/{config('Phone_Number_ID')}/messages"
            requests.post(
                url=url,
                data=payload,
                headers={'Authorization': f'Bearer {config("CLOUD_API_TOKEN")}'}
            )
        return data


    @action(detail=False, methods=['get'], url_path='fetch/(?P<course_id>[0-9a-f-]+)')
    def get_call_requests(self, request, course_id):
        """Get all call requests for a course."""
        #pylint: disable=no-member
        call_requests = CallRequest.objects.filter(course__id=course_id)
        serializer = CallRequestSerializer(call_requests, many=True)
        response = {
            "call_requests": serializer.data
        }
        return JsonResponse(response, status=200)


class LessonViewSet(viewsets.ModelViewSet):
    """Viewset for the Lesson model."""

    #pylint: disable=no-member
    queryset = Lesson.objects.all()
    permission_classes = (IsStaff,)
    renderer_classes = [JSONRenderer]
    serializer_class = LessonSerializer

    