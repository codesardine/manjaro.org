import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from .packages import update_x86_64, update_aarch64

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def today():
    return datetime.datetime.now()

def start():
    print("Scheduler started..\n")
    jobs = BackgroundScheduler()

    @jobs.scheduled_job(
            'interval', minutes=20,
            start_date=today() + datetime.timedelta(seconds=5)
            )
    def update_pkgs():
        print(f"Checking for package updates: {today()}")
        update_x86_64(None)
        update_aarch64(None)
        print("")

    jobs.start()
