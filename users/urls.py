from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, UserListView, UserDetailView, MeView, RegisterView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', MeView.as_view(), name='user-me'),
    path('register/',RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('refresh/', TokenRefreshView.as_view(), name='user-refresh')
]