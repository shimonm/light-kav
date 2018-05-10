import requests
import string
import random
import json

import exchange

# Lightning network node of public transportation company
url = 'http://rpc.blastoise.hackbtc18.offchain.rocks/'
username = 'api-token'
password = 'RwhKID54f30yQ'
headers = {'Content-Type': 'application/json'}


def _create_invoice(amt):
    # method that accepts an amount in milli satoshi
    # and returns the the payment request as bolt11 hash

    # random label is required for creaing an invoice
    label = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    data = '{"jsonrpc":"2.0","method":"invoice","params":[' + str(amt) + ',"' + label + '","my invoice desc"],"id":5}'

    response = requests.post(url, headers=headers, data=data, auth=(username, password))
    result = json.loads(response.content)
    bolt11 = result['result']['bolt11']
    return bolt11


def get_payment_request(amount):
    if amount <= 0:
        return None
    else:
        mili_satoshis = exchange.shekel_to_mili_satoshi(amount)
        return _create_invoice(mili_satoshis)