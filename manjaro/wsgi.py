import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manjaro.settings.production")

application = get_wsgi_application()

SETTINGS = os.environ.get("DJANGO_SETTINGS_MODULE")
if SETTINGS == "manjaro.settings.production":
    application = DjangoWhiteNoise(application)
