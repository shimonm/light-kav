from datetime import datetime, timedelta
import config
from db import

hour_and_a_half = timedelta(minutes=90)


def _get_this_week(today):
    day = today.day
    if 1 <= day <= 7:
        new_day = 1
    elif 8 <= day <= 14:
        new_day = 8
    elif 15 <= day <= 21:
        new_day = 15
    elif 22 <= day <= 28:
        new_day = 22
    else:
        new_day = 29

    return today.replace(day=new_day)


def calculate_amount(token, ride_code, time_stamp):
    all_user_rides = db.slect('select * from asdasdasd where token={} AND ride_code={}'.format(
                                token, ride_code
    )) or []

    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    this_week = _get_this_week(today)
    this_month = today.replace(day=1)

    this_month_rides = all_user_rides.filter(lambda x: x['time'] > this_month)
    payed_this_month = sum([int(r['amount']) for r in this_month_rides])
    if payed_this_month >= config.max_monthly_amount: # overflow fix
        return 0

    this_week_rides = this_month_rides.filter(lambda x: x['time'] > this_week)
    payed_this_week = sum([int(r['amount']) for r in this_week_rides])
    if payed_this_week >= config.max_weekly_amount:
        return 0

    today_rides = this_week.filter(lambda x: x['time'] > today)
    payed_today = sum([int(r['amount']) for r in today_rides])
    if payed_today >= config.max_daily_amount:
        return 0

    last_hour_and_a_half_rides = all_user_rides.filter(lambda x: x['time'] > now - hour_and_a_half)
    if last_hour_and_a_half_rides:
        return 0

    return config.codes_to_prices.get(ride_code, config.default_ride_price)


def get_curr_address():
    return 'abc'