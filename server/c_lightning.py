import requests
import config
import json


# Lightning network node of public transportation company
headers = {'Content-Type': 'application/json'}
url = config.charge_blastoise_api_url
username = config.charge_blastoise_api_username
password = config.charge_blastoise_api_password


def get_payment_request(amount, ride_code, user_id):
    if amount <= 0:
        return None
    else:
        payment_request, invoice_id = _create_charge_invoice(amount, ride_code, user_id)
        create_invoice_webhook(invoice_id)
        return payment_request


def _create_charge_invoice(amt, ride_code, customer_id):
    data = [
      ('msatoshi', amt),
      ('metadata[customer_id]', customer_id),
      ('metadata[ride_code]', ride_code),
    ]

    response = requests.post(url + 'invoice', data=data, auth=(username, password))

    invoice_json = json.loads(response.content)
    payment_request = invoice_json['payreq']
    invoice_id = invoice_json['id']
    return payment_request, invoice_id


# if a webhook for that invoice payment request was created returns true
def create_invoice_webhook(_id):
    data = [('url', '{}/onpayment'.format(config.public_url))]

    response = requests.post(url + 'invoice/' + _id + '/webhook', data=data, auth=(username, password))

    return response.text == 'Created'
