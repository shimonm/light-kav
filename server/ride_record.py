import json

from classes import Ride
import db


def _get_phone_ride_code(data):
    meta = data['metadata']
    phone, ride_code = meta['user_id'], meta['ride_code']
    return phone, ride_code


def record_payed_ride(data):
    import pprint
    pprint.pprint(data)
    phone, ride_code = _get_phone_ride_code(data)
    ride = Ride(None, phone, ride_code, data['msatoshi_received'], data['rhash'], None)
    db.insert_ride(ride)







import requests
import hashlib
import string
import random
import json

# Lightning network node of public transportation company
url = 'http://charge.blastoise.hackbtc18.offchain.rocks/'
username = 'api-token'
password = 'RwhKID54f30yQ'
headers = {
        'Content-Type': 'application/json',
    }


# method that accepts an amount in milli satoshis
# and returns the bolt11 hash as the payment request and is returned
# to the user
def create_invoice(amt):
    # random label is required for creaing an invoice
    label = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    data = '{"jsonrpc":"2.0","method":"invoice","params":[' + str(amt) + ',"' + label + '","my invoice desc"],"id":5}'

    response = requests.post(url, headers=headers, data=data, auth=(username, password))
    result = json.loads(response.content)
    # print(response.content)
    # print(response.text)
    print(result['result']['bolt11'])
    bolt11 = result['result']['bolt11']
    return bolt11


def create_charge_invoice(amt, ride_code, customer_id):
    data = [
      ('msatoshi', amt),
      ('metadata[customer_id]', customer_id),
      ('metadata[ride_code]', ride_code),
    ]

    response = requests.post(url + 'invoice', data=data, auth=(username, password))
    invoice_json = json.loads(response.content)

    return invoice_json


# returns true if webhook for that invoice payment request was created
def create_invoice_webhook(_id):
    data = [
      ('url', 'http://7abdb7b6.ngrok.io/onpayment'),
    ]

    response = requests.post(url + 'invoice/' + _id + '/webhook', data=data, auth=(username, password))

    return response.text == 'Created'


def on_payment_event(data):
    # save payment details to database
    # send confirmation to driver
    pass

def send_payreq_to_user(payreq):
    #send this payload to user so they can pay
    pass

invoice_json = create_charge_invoice("1", "444", "arbok")
print(invoice_json)
payreq = invoice_json['payreq']
_id = invoice_json['id']

boool = create_invoice_webhook(_id)

send_payreq_to_user(payreq)

