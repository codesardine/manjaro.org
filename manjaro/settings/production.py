from .base import *
import os

env = os.environ.copy()

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")

DATABASES = {
    'default': {
        'ENGINE': env("SQL_ENGINE"),
        'NAME': env("SQL_DATABASE"),
        'USER': env("SQL_USER"),
        'PASSWORD': env("SQL_PASSWORD"),
        'HOST': env("SQL_HOST"),
        'PORT': env("SQL_PORT"),
    }
}

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
SILENCED_SYSTEM_CHECKS = env('SILENCED_SYSTEM_CHECKS')
EMAIL_BACKEND = env('EMAIL_BACKEND')
DJANGO_ROOT = env('DJANGO_ROOT')

MIDDLEWARE = MIDDLEWARE + [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
COMPRESS_OFFLINE = True
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
