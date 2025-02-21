from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, EventRegistrationView


router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')


urlpatterns = [
    path('', include(router.urls)),
    path('<int:event_id>/register/', EventRegistrationView.as_view(),name='event-register')
]
