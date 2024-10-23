"""
Django settings for mba_business_plan .

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from socket import gethostname
from socket import gethostbyname
from datetime import timedelta
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
BPO_HOMES_SECRET_KEY = config('BPO_HOMES_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = eval(config("ALLOWED_HOSTS"))


ALLOWED_HOSTS.append(gethostbyname(gethostname()))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3RD PARTY
    "rest_framework",
    "drf_yasg",
    "import_export",
    "corsheaders",
    "rest_framework_simplejwt",
    "django_extensions",
    "rest_framework.authtoken",
    "django_filters",

    # LOCAL APPS
    "account",
    "farm",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = "account.User"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "html")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = eval(config("CSRF_TRUSTED_ORIGINS"))

CORS_ALLOWED_ORIGINS = eval(config("CORS_ALLOWED_ORIGINS"))


CORS_ALLOWED_ORIGINS.append('http://localhost:3000')

FRONTEND_URL = config("FRONTEND_URL")


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=config("ACCESS_TOKEN_LIFETIME", cast=int)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config("REFRESH_TOKEN_LIFETIME", cast=int)),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


FILEFIELD_MAX_LENGTH = config('FILEFIELD_MAX_LENGTH', default=10000)


FILE_MAX_SIZE = int(config("FILE_MAX_SIZE", 1024))


# Rest Frame work
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "core.utils.renders.CustomJsonRender",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
    "EXCEPTION_HANDLER": "core.utils.exception_handler.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": config("PAGE_SIZE", default=15, cast=int),

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_QUERYSTRING_AUTH = True
AWS_S3_SIGNATURE_VERSION = "s3v4"
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
    }


STATIC_URL = 'static/'


FILE_MAX_SIZE = config("FILE_MAX_SIZE", 1024, cast=int)
FILE_UPLOAD_STORAGE = config("FILE_UPLOAD_STORAGE", "local")  # local | s3

IS_USING_LOCAL_STORAGE = FILE_UPLOAD_STORAGE == "local"

if FILE_UPLOAD_STORAGE == "local":
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"
else:
    PUBLIC_MEDIA_LOCATION = "media/public/"
    PRIVATE_MEDIA_LOCATION = "media/private/"
    STATIC_LOCATION = "static/"

    AWS_ACCESS_KEY_ID = config["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = config["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = config["AWS_S3_REGION_NAME"]
    AWS_S3_CUSTOM_DOMAIN = config["AWS_S3_CUSTOM_DOMAIN"]
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}"
    STATICFILES_STORAGE = "core.storage_backends.StaticStorage"

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}"
    DEFAULT_FILE_STORAGE = "core.storage_backends.PublicMediaStorage"
    PRIVATE_FILE_STORAGE = "core.storage_backends.PrivateMediaStorage"

    FILE_UPLOAD_STORAGE = config("FILE_UPLOAD_STORAGE", "s3")
    AWS_PRESIGNED_EXPIRY = config("AWS_PRESIGNED_EXPIRY", 10, cast=int)
    FILE_MAX_SIZE = config("FILE_MAX_SIZE", 1024, cast=int)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SENDGRID_KEY = config("SENDGRID_KEY")
SERVER_EMAIL = config("EMAIL_HOST_USER")
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = SENDGRID_KEY
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")


SITE_ADMINS = config("SITE_ADMINS")
ADMIN_NAME, ADMIN_EMAIL = SITE_ADMINS.split(',', 1)

ADMINS = [(ADMIN_NAME, ADMIN_EMAIL)]

if not DEBUG:

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "include_html": True,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }
