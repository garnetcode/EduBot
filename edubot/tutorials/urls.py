"""URLs for tutorials app."""
from django.urls import path, include
from rest_framework import routers
#pylint: disable=import-error
from tutorials import views

router = routers.DefaultRouter()
router.register(r'tutorial', views.TutorialViewSet)
router.register(r'requests', views.CallRequestViewSet)

# define urls for tutorials app
urlpatterns = [
    path('', include(router.urls)),
]
