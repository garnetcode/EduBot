"""Views for the packages app."""
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework import viewsets
from django.http import JsonResponse

#pylint: disable=no-name-in-module
from users.permissions import IsStaff
from .models import Package
from .serializers import PackageSerializer

class PackageViewSet(viewsets.ModelViewSet):
    """Viewset for the Package model."""

    #pylint: disable=no-member
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (IsStaff, )
    renderer_classes = [JSONRenderer, ]

    #pylint: disable=unused-argument
    @action(detail=False, methods=['get'])
    def permissions(self, request):
        """Get all packages."""
        permissions ={
            '1': 'Curated Content',
            '2': 'Curated Content + Whatsapp Calls',
            '3': 'Curated Content + Whatsapp Calls + Zoom Calls'
        }
        return JsonResponse(permissions, status=200)

