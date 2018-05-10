import hashlib
import uuid


import db
from classes import UserExists


def _get_hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()


def register_new_user(user_phone_id, password):
    users = db.select_all_users().filter(lambda u: u.id == user_phone_id)
    if users:
        raise UserExists('user {} exists'.format(user_phone_id))
    else:
        token = _get_hash(password)
        return token
