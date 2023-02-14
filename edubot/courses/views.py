"""Courses Views"""
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action

#pylint: disable=no-name-in-module
from users.permissions import IsStaff
from users.models import User

#Local imports
from courses.serializers import ConversationSerializer, CourseSerializer
from courses.models import Course   

from tutorials.models import CallRequest, Lesson, Tutorial, Conversation, Message
from material.models import CourseMaterial
from payments.models import Payment



class CourseViewset(viewsets.ModelViewSet):
    """Course Viewset"""
    #pylint: disable=no-member
    queryset = Course.objects.all().exclude(code="COUT")
    permission_classes = (IsStaff, )
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "TUTOR":
            queryset = queryset.filter(instructors=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Override the create method."""
        serializer.save(instructors=[self.request.user])
        return super().perform_create(serializer)
    
    @action(detail=False, methods=['get'], url_path='all_stats')
    def all_stats(self, request):
        """Get all stats for a course"""
        print("here", Payment.objects.filter(payment_status='Paid').aggregate(total_earnings=Sum('amount')))

        data = {
            'staff':  User.objects.filter(role__in=['TUTOR', 'ADMIN']).count(),
            'students':  User.objects.filter(role='STUDENT').count(),
            'tutorials': Tutorial.objects.all().count(),
            'lessons': Lesson.objects.all().count(),
            'materials': CourseMaterial.objects.all().count(),
            'call_requests': CallRequest.objects.all().count(),
            'courses': Course.objects.all().count(),
            'payments': Payment.objects.all().count(),
            'total_earnings': float(Payment.objects.filter(payment_status='Paid').aggregate(total_earnings=Sum('amount'))['total_earnings']) or 0,

        }
        return JsonResponse(data, status=200)

    @action(detail=False, methods=['get'], url_path='stats/(?P<course_id>[0-9a-f-]+)')
    def stats(self, request, course_id):
        """Get stats for a course"""
        #pylint: disable=no-member
        course = Course.objects.get(id=course_id)
        #pylint: disable=no-member
        students = User.objects.filter(role='STUDENT', enrolled_courses=course)
        #pylint: disable=no-member
        tutorials = Tutorial.objects.filter(course=course)
        #pylint: disable=no-member
        lessons = Lesson.objects.filter(tutorial_class__in=tutorials)
        #pylint: disable=no-member
        materials = CourseMaterial.objects.filter(course=course)
        #pylint: disable=no-member
        call_requests = CallRequest.objects.filter(course=course)

        data = {
            'course': course.name,
            'students': students.count(),
            'tutorials': tutorials.count(),
            'lessons': lessons.count(),
            'materials': materials.count(),
            'call_requests': call_requests.count(),
        }
        return JsonResponse(data, status=200)
    
    


class ConversationViewset(viewsets.ModelViewSet):
    """Conversation Viewset"""
    #pylint: disable=no-member
    queryset = Conversation.objects.all()
    permission_classes = (IsStaff, )
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "TUTOR":
            queryset = queryset.filter(course__instructors=self.request.user)
        return queryset

    @action(detail=False, methods=['get'], url_path='fetch/(?P<course_id>[0-9a-f-]+)')
    def get_by_course(self, request, course_id):
        """Get all call requests for a course."""
        #pylint: disable=no-member
        print("here", course_id)
        serializer = self.serializer_class(self.queryset.filter(course__id=course_id), many=True)
        response = {
            "conversations": serializer.data
        }
        return JsonResponse(response, status=200)

    # post message, takes in a conversation id and a message
    @action(detail=False, methods=['post'], url_path='post_message')
    def post_message(self, request):
        """Post a message"""
        #pylint: disable=no-member
        conversation = Conversation.objects.get(id=request.data['conversation_id'])

        if conversation:
            if self.request.user.role == "TUTOR":
                if self.request.user not in conversation.course.instructors.all():
                    return JsonResponse({'message': 'You are not allowed to post in this conversation'}, status=400)
            #pylint: disable=no-member
            conversation.post_message(request.user, request.data['message'])
            return JsonResponse({'message': 'Message sent successfully'}, status=200)
        return JsonResponse({'message': 'Conversation not found'}, status=400)
        