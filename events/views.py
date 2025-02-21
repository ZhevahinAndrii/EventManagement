from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Event
from .serializers import EventRegistrationSerializer, EventSerializer, EventUnregistrationSerializer
from users.permissions import IsAdminOrCurrentUserOrReadOnly



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().prefetch_related('participants').select_related('organizer')
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrCurrentUserOrReadOnly]


class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description='Register the authenticated user(or another user if admin) for an event.',
            request_body=EventRegistrationSerializer,
            responses={
                201: EventSerializer(),
                400: openapi.Response('Validation error'),
                404: openapi.Response('Event not found')
            }
    )
    def post(self, request, event_id:int):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventRegistrationSerializer(data=request.data, context={'request': request, 'event': event})

        if serializer.is_valid():
            event = serializer.save()

            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
            operation_description='Unregister the authenticated user(or another user if admin) for an event',
            request_body=EventRegistrationSerializer,
            responses={
                400: openapi.Response('Validation error'),
                404: openapi.Response('Event not found')
            }
    )
    def delete(self, request, event_id:int):
        event = get_object_or_404(Event, id=event_id)
        serializer = EventUnregistrationSerializer(data=request.data, context={'request': request, 'event': event})

        if serializer.is_valid():
            event = serializer.save()
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


