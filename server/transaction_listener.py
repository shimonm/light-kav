import requests
import hashlib
import string
import random
import json

# Lightning network node of public transportation company
url = 'http://rpc.blastoise.hackbtc18.offchain.rocks/'
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

def on_payment_event(data):
    # save payment details to database
    # send confirmation to driver
    pass