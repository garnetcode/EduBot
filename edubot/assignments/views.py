"""Assignment Views"""
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action


#pylint: disable=no-name-in-module
from users.permissions import IsStaff

#Local imports
from assignments.serializers import AssignmentSerializer, PendingWorkSerializer
from assignments.models import Assignment, PendingWork

class AssignmentViewset(viewsets.ModelViewSet):
    """Assignment Viewset"""
    #pylint: disable=no-member
    queryset = Assignment.objects.all()
    permission_classes = (IsStaff, )
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "ADMIN":
            return queryset
        return queryset.filter(course__instructors__in=self.request.user)

    def perform_create(self, serializer):
        """Override the create method."""
        serializer.save()
        return super().perform_create(serializer)
    
    #get assignments by course
    @action(detail=False, methods=['get'], url_path='fetch/(?P<course_id>[0-9a-f-]+)')
    def fetch(self, request, course_id):
        """Fetch an assignment by course and step."""
        #pylint: disable=no-member
        assignments = Assignment.objects.filter(referenced_work__course=course_id)
        serializer = AssignmentSerializer(assignments, many=True)
        data = {
            "assignments": serializer.data
        }
        return JsonResponse(data, status=200)
    
    @action(detail=False, methods=['get'], url_path='fetch/outsourced')
    def outsourced(self, request):
        """Fetch an assignment by course and step."""
        #pylint: disable=no-member
        assignments = Assignment.objects.filter(assignment_type="Outsourced")
        serializer = AssignmentSerializer(assignments, many=True)
        data = {
            "assignments": serializer.data
        }
        return JsonResponse(data, status=200)
    
class PendingWorkViewset(viewsets.ModelViewSet):
    """Pending Work Viewset"""
    #pylint: disable=no-member
    queryset = PendingWork.objects.all()
    permission_classes = (IsStaff, )
    serializer_class = PendingWorkSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "TUTOR":
            queryset = queryset.filter(course__instructors=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Override the create method."""
        serializer.save(uploaded_by=self.request.user)
        return super().perform_create(serializer)
    
    #get pending work by course
    @action(detail=False, methods=['get'], url_path='filter/(?P<course_id>[0-9a-f-]+)')
    def filter(self, request, course_id):
        """Fetch an assignment by course and step."""
        #pylint: disable=no-member
        pending_works = PendingWork.objects.filter(course=course_id)
        serializer = PendingWorkSerializer(pending_works, many=True)
        data = {
            "pending_works": serializer.data
        }
        return JsonResponse(data, status=200)