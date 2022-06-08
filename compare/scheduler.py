jobs = None

def start():
    global jobs
    print("run jobs.scheduled_job ?...")
    if jobs:
        return
    print("START jobs.scheduled_job(update_packages)")
    from apscheduler.schedulers.background import BackgroundScheduler
    from .packages import update_packages, update_arm_packages
    from .models import Package, armPackage, Updates
    import datetime

    now = datetime.datetime.now()+datetime.timedelta(seconds=2)
    TIMER = 30

    jobs = BackgroundScheduler()
    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def update():
        update_packages(Package, Updates)

    now = datetime.datetime.now()+datetime.timedelta(minutes=TIMER//2)
    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def arm_update():
        update_arm_packages(armPackage, Updates)

    jobs.start()