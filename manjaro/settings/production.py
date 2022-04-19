from .base import *
import os
env = os.environ.copy()

SECRET_KEY = env("SECRET_KEY")
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

RECAPTCHA_PUBLIC_KEY = env['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = env['RECAPTCHA_PRIVATE_KEY']

try:
    from .local import *
except ImportError:
    pass
