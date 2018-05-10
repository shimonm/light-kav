import json

from classes import Ride
import db

_data = {
    u'created_at': 1525980441,
    u'description': u'Lightning Charge Invoice',
    u'expires_at': 1525984041,
    u'id': u'0cgCQ7WNyGW6wOq4CL0Sq',
    u'metadata': None,
    u'msatoshi': u'1000',
    u'msatoshi_received': u'1000',
    u'paid_at': 1525980508,
    u'pay_index': 5,
    u'payreq': u'lnbcrt10n1pd0f8gepp55wpepmdl2hucfy7w363kr9kc3hnt30yl3w9gfph0ejpxugdffyrsdp8f35kw6r5de5kueeqgd5xzun8v5syjmnkda5kxegcqpxjr7a50cmqysfz24zsv0znj0tavwtvza6ugwy55ljsnhewwhjh6944pww25pahusvhfuw2aasnsyff0qrnezhzfy5vvxpp3flm424c0sqzluq7g',
    u'quoted_amount': None,
    u'quoted_currency': None,
    u'rhash': u'a38390edbf55f98493ce8ea36196d88de6b8bc9f8b8a8486efcc826e21a94907',
    u'status': u'paid'
}


def _get_phone_ride_code(data):
    string = data['description']
    hidden_data = json.loads(string)
    phone, ride_code = hidden_data['user_id'], hidden_data['ride_code']
    return phone, ride_code


def record_payed_ride(data):
    phone, ride_code = _get_phone_ride_code(data)
    ride = Ride(None, phone, ride_code, data['msatoshi_received'], data['rhash'], None)
    db.insert_ride(ride)
