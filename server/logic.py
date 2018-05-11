from datetime import datetime, timedelta
import config
import db

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


def calculate_amount_and_saved(token, ride_code):
    ride_price = config.codes_to_prices.get(ride_code, config.default_ride_price)
    amount = ride_price

    all_user_rides = db.select_rides_by_user_token(token) or []
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    this_week = _get_this_week(today)
    this_month = today.replace(day=1)

    this_month_rides = [r for r in all_user_rides if r.ride_datetime > this_month]
    payed_this_month = sum([int(r.amount_paid) for r in this_month_rides])
    print 'payed_this_month', payed_this_month
    print 'config.max_monthly_amount', config.max_monthly_amount
    print
    if payed_this_month >= config.max_monthly_amount:
        amount = 0
    if payed_this_month > config.max_monthly_amount - ride_price:
        diff = config.max_monthly_amount - payed_this_month
        amount = diff

    this_week_rides = [r for r in this_month_rides if r.ride_datetime > this_week]
    payed_this_week = sum([int(r.amount_paid) for r in this_week_rides])
    print 'payed_this_week', payed_this_week
    print 'config.max_weekly_amount', config.max_weekly_amount
    print
    if payed_this_week >= config.max_weekly_amount:
        amount = 0
    if payed_this_week > config.max_weekly_amount - ride_price:
        diff = config.max_weekly_amount - payed_this_week
        amount = diff

    today_rides = [r for r in this_week_rides if r.ride_datetime > today]
    payed_today = sum([int(r.amount_paid) for r in today_rides])
    print 'payed_today', payed_today
    print 'config.max_daily_amount', config.max_daily_amount
    print
    if payed_today >= config.max_daily_amount:
        amount = 0
    if payed_today >= config.max_daily_amount - ride_price:
        diff = config.max_daily_amount - payed_today
        amount = diff

    # for the demo only
    demo = True
    if demo:
        ten_seconds = timedelta(seconds=10)
        last_ten_seconds_rides = [r for r in all_user_rides if r.ride_datetime > now - ten_seconds]
        print 'last_ten_seconds_rides:', last_ten_seconds_rides
        print
        if last_ten_seconds_rides:
            amount = 0
    else:
        last_hour_and_a_half_rides = [r for r in all_user_rides if r.ride_datetime > now - hour_and_a_half]
        print 'last_hour_and_a_half_rides:', last_hour_and_a_half_rides
        print
        if last_hour_and_a_half_rides:
            amount = 0

    if amount < 0:
        raise Exception('amount to charge is {}'.format(amount))
    if amount == 0:
        db.insert_empty_ride(token, ride_code)

    saved = ride_price - amount
    return amount, saved
