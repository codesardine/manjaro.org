import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from .packages import update_x86_64, update_aarch64

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


def start():
    print("Scheduler started..\n")
    today = datetime.datetime.now()
    now = today+datetime.timedelta(seconds=2)
    jobs = BackgroundScheduler()

    @jobs.scheduled_job('interval', minutes=20, start_date=now)
    def update_pkgs():
        print(f"Updating packages at: {today}")
        update_x86_64(None)
        update_aarch64(None)
        print("")

    jobs.start()
