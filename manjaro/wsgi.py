import os
from django.core.wsgi import get_wsgi_application
from manjaro.settings.base import STATIC_ROOT
from whitenoise import WhiteNoise


#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manjaro.settings.production")

application = get_wsgi_application()

SETTINGS = os.environ.get("DJANGO_SETTINGS_MODULE")
if SETTINGS == "manjaro.settings.production":
    application = WhiteNoise(application, root=STATIC_ROOT)
