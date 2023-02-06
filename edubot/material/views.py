"""Material Views"""
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

#pylint: disable=no-name-in-module
from users.permissions import IsStaff


#Local imports
from .serializers import MaterialSerializer
from .models import CourseMaterial


class MaterialViewset(viewsets.ModelViewSet):
    """Material Viewset"""
    #pylint: disable=no-member
    queryset = CourseMaterial.objects.all()
    permission_classes = (IsStaff, )
    serializer_class = MaterialSerializer

    def get_queryset(self):
        """Override the get_queryset method."""
        queryset = super().get_queryset()
        if self.request.user.role == "TUTOR":
            queryset = queryset.filter(course__instructors=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Override the create method."""
        serializer.save()
        return super().perform_create(serializer)
    
    #get materials by course
    @action(detail=False, methods=['get'], url_path='filter/(?P<course_id>[0-9a-f-]+)')
    def filter(self, request, course_id):
        """Fetch a material by course."""
        #pylint: disable=no-member
        materials = CourseMaterial.objects.filter(course=course_id)
        serializer = MaterialSerializer(materials, many=True)
        data = {
            "materials": serializer.data
        }
        return JsonResponse(data, status=200)