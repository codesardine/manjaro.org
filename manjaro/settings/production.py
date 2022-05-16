from .base import *
import os

DEBUG=True

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE"),
        'NAME': os.environ.get("SQL_DATABASE"),
        'USER': os.environ.get("SQL_USER"),
        'PASSWORD': os.environ.get("SQL_PASSWORD"),
        'HOST': os.environ.get("SQL_HOST"),
        'PORT': os.environ.get("SQL_PORT"),
    }
}

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
SILENCED_SYSTEM_CHECKS = os.environ.get('SILENCED_SYSTEM_CHECKS')
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
DJANGO_ROOT = os.environ.get('DJANGO_ROOT')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
#CONTENT_TYPE_NO_SNIFF=True
#SECURE_SSL_REDIRECT=True
#X_FRAME_OPTIONS='DENY'
#XSS_PROTECTION=True

try:
    from .local import *
except ImportError:
    pass
