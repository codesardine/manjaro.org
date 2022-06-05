from django.apps import AppConfig


class CompareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compare'


    def ready(self):
        """ 
            wait for app to be ready so we can manipulate models
            #FIXME this will probaly execute once per worker wich is not ideal
        # """
        from compare import scheduler
        scheduler.start()
            
            

