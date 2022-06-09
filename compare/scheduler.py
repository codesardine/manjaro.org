def start():    
    print("Scheduler started..\n")
    from apscheduler.schedulers.background import BackgroundScheduler
    from .packages import update_packages, update_arm_packages
    from .models import Package, armPackage, Updates
    import datetime

    now = datetime.datetime.now()+datetime.timedelta(seconds=2)
    TIMER = 30

    jobs = BackgroundScheduler()
    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def update():
        print("Packages timer fired")
        update_packages(Package, Updates)

    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def arm_update():
        print("ARM Packages timer fired")
        update_arm_packages(armPackage, Updates)

    jobs.start()
