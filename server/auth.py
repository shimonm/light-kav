import hashlib
import uuid


import config
import db
from classes import UserExists, User


def _get_hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()


def register_new_user(user_phone_id, password):
    users = [u for u in db.select_all_users() if u.id == user_phone_id]
    if config.registration_feature_complete:

        if users:
            raise UserExists('user {} exists'.format(user_phone_id))
        else:
            token = _get_hash(password)
            user = User(user_phone_id, '123123123', user_phone_id, user_phone_id, None, token)
            db.insert_user(user)
            return token

    else:

        if users:
            return users[0].token
        else:
            token = _get_hash(password)
            user = User(user_phone_id, '123123123', user_phone_id, user_phone_id, None, token)
            db.insert_user(user)
        return token
