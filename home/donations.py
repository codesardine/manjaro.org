import requests, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Donations


def get_request(endpoint, headers={}):
    headers = {'Accept': 'application/json'}
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_exchange_rates(_from, to, ammount):
    endpoint = f'https://api.exchangerate.host/convert?from={_from}&to={to}&amount={ammount}&places=0'
    data = get_request(endpoint)
    return data

def get_uk_info():
    endpoint = 'https://opencollective.com/manjaro-uk.json'
    data = get_request(endpoint)
    balance = data["balance"]
    rates = get_exchange_rates(data["currency"], "EUR", balance)
    data["total"] = rates["result"]
    return data

def get_us_info():
    endpoint = 'https://opencollective.com/manjaro-us.json'
    data = get_request(endpoint)
    balance = data["balance"]
    rates = get_exchange_rates(data["currency"], "EUR", balance)
    data["total"] = rates["result"]
    return data

def get_eu_info():
    endpoint = 'https://opencollective.com/manjaro.json'
    data = get_request(endpoint)
    data["total"] = data["balance"]
    return data

def get_collectives():
    eu = get_eu_info()
    us = get_us_info()
    uk = get_uk_info()

    balance = eu["total"] + us["total"] + uk["total"]
    backers = eu["backersCount"] + us["backersCount"] + uk["backersCount"]

    return{
        "balance": balance,
        "backers": backers
    }

def sheduler_start():
    jobs = BackgroundScheduler()
    now = datetime.datetime.now()+datetime.timedelta(seconds=2)
    @jobs.scheduled_job('interval', days=1, start_date=now)
    def update():
        data = get_collectives()
        Donations.objects.update(
            backers=data["backers"], balance=data["balance"]
        )
    jobs.start()

