import hashlib
import uuid


import db
# from classes import UserExists


def _get_hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()


def register_new_user(user_phone_id, password):
    users = [u for u in db.select_all_users() if u.id == user_phone_id]
    # if users:
    #     raise UserExists('user {} exists'.format(user_phone_id))
    # else:

    ##### for now this is the behavior
    if users:
        return users[0].token
    ######
    token = _get_hash(password)
    return token
