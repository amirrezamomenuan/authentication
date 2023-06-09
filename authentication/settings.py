from pathlib import Path
from decouple import config, Csv

from .logging import LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
JWT_AUTHENTICATION_KEY = config('JWT_AUTHENTICATION_KEY')
ACCESS_TOKEN_EXPIRATION_TIME = config('ACCESS_TOKEN_EXPIRATION_TIME', cast=int)
REFRESH_TOKEN_EXPIRATION_TIME = config('REFRESH_TOKEN_EXPIRATION_TIME', cast=int)

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

OTP_SECRET_TOKEN = config('OTP_SECRET_TOKEN')
OTP_VERIFICATION_SMS_URL = config('OTP_VERIFICATION_SMS_URL')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'AppUser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'authentication.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'authentication.wsgi.application'


# Database
DB_ENGINE = 'django.db.backends.mysql'


DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'HOST': config('DB_HOST'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'PORT': config('DB_PORT'),
        'TEST': {
            'NAME': config('DB_TEST_NAME')
        }
    }
}

CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REQUEST_LIMIT = config('LOGIN_REQUEST_LIMIT', cast=int)
VERIFICATION_CODE_LENGTH = config('VERIFICATION_CODE_LENGTH', cast=int)
VERIFICATION_CODE_EXPIRE_TIME_SECONDS = config('VERIFICATION_CODE_EXPIRE_TIME_SECONDS', cast=int)
