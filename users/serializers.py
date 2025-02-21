from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    events_organized = serializers.StringRelatedField(source='organized_events', many=True,read_only=True)
    events_participated = serializers.StringRelatedField(source='participated_events', many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'last_login', 'date_joined', 'events_organized', 'events_participated']
        extra_kwargs = {field: {'required': False} for field in ['email', 'username', 'first_name', 'last_name', 'last_login','date_joined']}
        extra_kwargs.update({field:{'read_only':True} for field in ['last_login', 'is_superuser','date_joined']})
       
        
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)
    admin_additional_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_superuser','password_confirm','admin_additional_password']
        extra_kwargs = {field:{'required':False} for field in ['id', 'username', 'email', 'first_name', 'last_name','is_superuser']}
        extra_kwargs['id'] = {'read_only':True}
        extra_kwargs.update({field:{'write_only':True} for field in ['password','password_confirm', 'admin_addtional_password']})

    def validate(self, data):
        
        if not data.get('email') and not data.get('username'):
            raise ValidationError({'email': ['Either email or username is required.']})
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError({'password': ['Passwords do not match.']})

        if data.get('admin_additional_password') != settings.ADMIN_ADDITIONAL_PASSWORD:
            raise ValidationError({'admin_password': 'Admin password is incorrect'})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data.pop('admin_additional_password')
        validated_data['email'] = validated_data.get('email') if validated_data.get('email') else None
        try:
            user = User.objects.create_user(**validated_data, is_staff=bool(validated_data.get('is_superuser')))
            return user
        except Exception as e:
            raise ValidationError(e)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self,data):
        login, password = data.get('login'), data.get('password')

        user = User.objects.filter(Q(email=login) | Q(username=login)).first()
        if not user:
            raise serializers.ValidationError({'login': 'User not found'})
        
        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password'})
        
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
