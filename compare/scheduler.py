def start():
    from apscheduler.schedulers.background import BackgroundScheduler
    from .packages import update_packages, update_arm_packages
    from .models import Package, armPackage, Updates
    import datetime

    NOW = datetime.datetime.now()+datetime.timedelta(seconds=2)

    jobs = BackgroundScheduler() 
    @jobs.scheduled_job('interval', minutes=60, start_date=NOW)
    def update():
        update_packages(Package, Updates)

    @jobs.scheduled_job('interval', minutes=60, start_date=NOW)
    def arm_update():
        update_arm_packages(armPackage, Updates)

    jobs.start()