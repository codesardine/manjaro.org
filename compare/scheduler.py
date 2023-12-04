import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .packages import update_x86_64, update_aarch64


def start():  
    print("Scheduler started..\n")
    now = datetime.datetime.now()+datetime.timedelta(seconds=2)
    jobs = BackgroundScheduler()

    @jobs.scheduled_job('interval', minutes=15, start_date=now)
    def update_pkgs():
        print("Packages timer fired")
        update_x86_64(None)
        update_aarch64(None)

    jobs.start()
