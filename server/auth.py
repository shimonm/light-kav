import hashlib
import uuid


import db
from classes import UserExists, User


def _get_hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()


def register_new_user(user_phone_id, password):
    users = [u for u in db.select_all_users() if u.id == user_phone_id]
    # if users:
    #     raise UserExists('user {} exists'.format(user_phone_id))
    # else:

    # for now this is the behavior
    if users:
        print 'found users'
        return users[0].token
    else:
        print 'creating'
        token = _get_hash(password)
        user = User(user_phone_id, '123123123', user_phone_id, user_phone_id, None, token)
        db.insert_user(user)
    return token
