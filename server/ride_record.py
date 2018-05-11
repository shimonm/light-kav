import requests
import string
import random
import json

from classes import Ride
import db


def _get_phone_ride_code(data):
    meta = data['metadata']
    phone, ride_code = meta['customer_id'], meta['ride_code']
    return phone, ride_code


def record_payed_ride(data):
    phone, ride_code = _get_phone_ride_code(data)
    ride = Ride(None, phone, ride_code, data['msatoshi_received'], data['rhash'], None)
    db.insert_ride(ride)

