import os

from django.core.wsgi import get_wsgi_application

if "DEBUG" in os.environ:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manjaro.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manjaro.settings.dev")

application = get_wsgi_application()
