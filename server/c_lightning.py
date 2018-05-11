# import requests
# import string
# import random
# import json
#
# import exchange
#
# # Lightning network node of public transportation company
# url = 'http://rpc.blastoise.hackbtc18.offchain.rocks/'
# username = 'api-token'
# password = 'RwhKID54f30yQ'
# headers = {'Content-Type': 'application/json'}
#
#
# def _create_invoice(amt):
#     # method that accepts an amount in milli satoshi
#     # and returns the the payment request as bolt11 hash
#
#     # random label is required for creaing an invoice
#     label = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
#
#     data = '{"jsonrpc":"2.0","method":"invoice","params":[' + str(amt) + ',"' + label + '","my invoice desc"],"id":5}'
#
#     response = requests.post(url, headers=headers, data=data, auth=(username, password))
#     result = json.loads(response.content)
#     bolt11 = result['result']['bolt11']
#     return bolt11
#
#
# def get_payment_request(amount):
#     if amount <= 0:
#         return None
#     else:
#         mili_satoshis = exchange.shekel_to_mili_satoshi(amount)
#         return _create_invoice(mili_satoshis)
#
#
#
#
from classes import Ride
import db
import exchange
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
# def create_invoice(amt):
#     # random label is required for creaing an invoice
#     label = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
#
#     data = '{"jsonrpc":"2.0","method":"invoice","params":[' + str(amt) + ',"' + label + '","my invoice desc"],"id":5}'
#
#     response = requests.post(url, headers=headers, data=data, auth=(username, password))
#     result = json.loads(response.content)
#     # print(response.content)
#     # print(response.text)
#     print(result['result']['bolt11'])
#     bolt11 = result['result']['bolt11']
#     return bolt11
def get_payment_request(amount, ride_code, user_id):
    if amount <= 0:
        ride = Ride(None, user_id, ride_code, amount, None, None)
        db.insert_ride(ride)
        return None
    else:
        mili_satoshis = exchange.shekel_to_mili_satoshi(amount)
        # return _create_invoice(mili_satoshis)
        payment_request, invoice_id = _create_charge_invoice(mili_satoshis, ride_code, user_id)
        create_invoice_webhook(invoice_id)
        return payment_request


def _create_charge_invoice(amt, ride_code, customer_id):
    data = [
      ('msatoshi', amt),
      ('metadata[customer_id]', customer_id),
      ('metadata[ride_code]', ride_code),
    ]

    response = requests.post(url + 'invoice', data=data, auth=(username, password))

    print url + 'invoice'
    print data
    print amt

    invoice_json = json.loads(response.content)
    payment_request = invoice_json['payreq']
    invoice_id = invoice_json['id']
    return payment_request, invoice_id


# returns true if webhook for that invoice payment request was created
def create_invoice_webhook(_id):
    data = [
      ('url', 'http://7abdb7b6.ngrok.io/onpayment'),
    ]

    response = requests.post(url + 'invoice/' + _id + '/webhook', data=data, auth=(username, password))

    return response.text == 'Created'
