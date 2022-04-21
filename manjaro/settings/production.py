from pickle import TRUE
from .base import *
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

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

MIDDLEWARE = MIDDLEWARE + [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
COMPRESS_OFFLINE = TRUE
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]

CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR + "/staticfiles"

try:
    from .local import *
except ImportError:
    pass
