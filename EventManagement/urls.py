from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet



schema_view = get_schema_view(openapi.Info(
    title='EventManagementAPI',
    default_version='v1',
    description='Swagger Documentation for EventManagementAPI',
    contact=openapi.Contact(email='andreyzhevagin@gmail.com'),
),
public=True,
permission_classes=(permissions.IsAuthenticatedOrReadOnly,))


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("users/", include('users.urls')),
    path('events/', include("events.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
