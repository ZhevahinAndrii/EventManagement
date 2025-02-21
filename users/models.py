from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self,username:str | None = None, email:str | None = None,password:str | None = None, **extra_fields):
        if not password:
            raise ValidationError({'password': 'Password must be set'})
        
        if email:
            print('normalizing')
            email = self.normalize_email(email)
        try:
            user: "User" = self.model(username=username, email=email, password=password,**extra_fields)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise ValidationError({'error':str(e)})

class User(AbstractUser):
    email = models.EmailField(
        blank=True, 
        null=True, 
        error_messages={'unique': 'A user with that email already exists.'},)
    username = models.CharField(
        max_length=150,
        blank=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "A user with that username already exists.",
        })
    
    objects = CustomUserManager()

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('email',), name='user_email_unique_constraint'),
            models.UniqueConstraint(fields=('username',),name='user_username_unique_constraint')
        )
        indexes = (
            models.Index(fields=('email',), name='user_email_index'),
            models.Index(fields=('username',),name='user_username_index')
        )
    
    def clean(self):
        if not self.username and not self.email:
            raise ValidationError({'email': 'Email or username is needed for user'})
    
        if not self.email and len(self.username.split('@')) > 1:
            self.email = self.username
        if self.email:
            print('Checking')
            self.email = self.__class__.objects.normalize_email(self.email)
        if not self.username:
            self.username = self.email
    
    def save(self ,*args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
