def start():    
    print("Scheduler started..\n")
    from apscheduler.schedulers.background import BackgroundScheduler
    from .packages import update_x86_64, update_aarch64
    import datetime

    now = datetime.datetime.now()+datetime.timedelta(seconds=2)
    TIMER = 1

    jobs = BackgroundScheduler()
    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def x86_64_update():
        print("Packages timer fired")
        update_x86_64(None)

    @jobs.scheduled_job('interval', minutes=TIMER, start_date=now)
    def aarch64_update():
        print("ARM Packages timer fired")
        update_aarch64(None)

    jobs.start()
