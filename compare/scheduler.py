import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .packages import update_x86_64, update_aarch64


def start():
    print("Scheduler started..\n")
    today = datetime.datetime.now()
    now = today+datetime.timedelta(seconds=2)
    jobs = BackgroundScheduler()

    @jobs.scheduled_job('interval', minutes=15, start_date=now)
    def update_pkgs():
        print(f"Updating packages at: {today}")
        update_x86_64(None)
        print("")
        update_aarch64(None)
        print("")

    jobs.start()
