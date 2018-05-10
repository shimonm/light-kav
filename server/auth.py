import hashlib
import uuid


def _get_hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password + salt).hexdigest()


def _search_user(username):
    # search db
    return []


def register_new_user(name, password):
    if _search_user(name):
        token = _get_hash(password)
        return True, token
    else:
        return False, None