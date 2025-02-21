from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializers import  LoginSerializer, UserSerializer, RegistrationSerializer
from .permissions import IsAdminOrCurrentUserOrReadOnly


User = get_user_model()


class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Getting actual user's info",
        responses={
            200: UserSerializer(),
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all().prefetch_related('participated_events').prefetch_related('organized_events')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all().prefetch_related('participated_events').prefetch_related('organized_events')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrCurrentUserOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    @swagger_auto_schema(
        operation_description='Updating user`s info',
        request_body=UserSerializer,
        responses={
            200: UserSerializer(),
            400: "Validation error",
            404: "User not found"
        }
    )
    def put(self, request,*args,**kwargs):
        return super().put(request,*args,**kwargs)

    @swagger_auto_schema(
        operation_description='Partial updating of user`s info',
        request_body=UserSerializer,
        responses={
            200: UserSerializer(),
            400: "Validation error",
            404: "User not found"
        }
    )
    def patch(self,request,*args,**kwargs):
        return super().put(request, *args,**kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)
        except Exception as e:
            raise DRFValidationError(e)
        

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description='Registration and login of a new user',
        request_body=RegistrationSerializer,
        responses={
            201: TokenRefreshSerializer(),
            400: 'Validation error'
        }
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({'access': access, 'refresh': str(refresh)},status=status.HTTP_201_CREATED)
        except DRFValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User's login",
        request_body=LoginSerializer(),
        responses={
            201: TokenRefreshSerializer(),
            400: 'Validation error'
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
