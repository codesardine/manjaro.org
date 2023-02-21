from django.apps import AppConfig
import sys

class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        """ 
            wait for app to be ready so we can manipulate models
            #FIXME this will probaly execute once per worker wich is not ideal
        """
        if "runserver" in sys.argv or any("gunicorn" in cmd for cmd in sys.argv):
           from .donations import sheduler_start
           sheduler_start()
