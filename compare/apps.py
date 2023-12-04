import os
import sys
from django.apps import AppConfig


class CompareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compare'

    def ready(self):
        """ 
            wait for app to be ready so we can manipulate models
            #FIXME this will probaly execute once per worker wich is not ideal
        """
        if "runserver" in sys.argv or any(
            "gunicorn" in cmd for cmd in sys.argv
        ):
            run_once = os.environ.get("SCHEDULER_EXECUTED")
            if run_once is not None:
                return

            os.environ["SCHEDULER_EXECUTED"] = "True"
            from compare import scheduler
            scheduler.start()
