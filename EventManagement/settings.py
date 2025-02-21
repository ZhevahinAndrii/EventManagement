import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv



BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_ENVIRONMENT = os.getenv('DJANGO_ENV', 'dev').lower()

if DJANGO_ENVIRONMENT not in {'dev','prod'}:
    raise ValueError(f'Invalid DJANGO_ENV: {DJANGO_ENVIRONMENT}. Must be "dev" or "prod"')

env_path = os.path.join(BASE_DIR,f"{DJANGO_ENVIRONMENT}.env")
load_dotenv(env_path)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG','true').lower() == 'true'


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


INSTALLED_APPS = [
    # default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # custom apps
    'users.apps.UsersConfig',
    'events.apps.EventsConfig',

    # third-party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware"
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    'http://127.0.0.1:3000', # may be useful for frontend on 3000 port for dev and prod versions
    'http://frontend:3000'
]

ROOT_URLCONF = "EventManagement.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "EventManagement.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = os.getenv('LANGUAGE_CODE','en-us')
TIME_ZONE = os.getenv('TIME_ZONE','UTC')
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION' : True,
    'AUTH_HEADER_TYPES': ('Bearer',)
}


ADMIN_ADDITIONAL_PASSWORD = os.getenv('ADMIN_ADDITIONAL_PASSWORD')