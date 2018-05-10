

class Ride:
    def __init__(self, _id, phone, ride_code, amount_paid, payment_hash, ride_datetime):
        self.id = _id
        self.user_id = phone
        self.ride_code = ride_code
        self.amount_paid = amount_paid
        self.payment_hash = payment_hash
        self.ride_datetime = ride_datetime


class User:
    def __init__(self, _id, government_id, last_name, first_name, created, token):
        self.id = _id
        self.government_id = government_id
        self.last_name = last_name
        self.first_name = first_name
        self.created = created
        self.token = token


class NoSuchUser(Exception):
    pass


class UserExists(Exception):
    pass
