import psycopg2

from classes import Ride, User, NoSuchUser

url = '192.168.1.5'
# url = '192.168.8.113'
dbname = 'lightkavdb'
rides = 'rides'
users = 'user_base'

_connection = psycopg2.connect("dbname='{}' user='postgres' host='{}' password='lightkavwins'".format(dbname, url))


def select_all_users():
    cur = _connection.cursor()
    cur.execute('SELECT * from user_base')
    rows = cur.fetchall()
    return [User(*r) for r in rows]


def select_user_by_token(token):
    cur = _connection.cursor()
    cur.execute("""SELECT * from user_base WHERE token=\'{}\'""".format(token))
    rows = cur.fetchall()
    if not rows:
        raise NoSuchUser('no user with token {}'.format(token))
    return rows[0]


def select_rides_by_user_token(user_token):
    cur = _connection.cursor()
    user_id = select_user_by_token(user_token)[0]
    cur.execute("SELECT * from rides WHERE user_id=\'{}\'".format(user_id))
    rows = cur.fetchall()
    return [Ride(*r) for r in rows]


def select_all_rides():
    cur = _connection.cursor()
    cur.execute('SELECT * from rides')
    rows = cur.fetchall()
    return [Ride(*r) for r in rows]


def insert_empty_ride(token, ride_code):
    user = select_user_by_token(token)
    user_obj = User(*user)
    cur = _connection.cursor()
    cur.execute("""INSERT INTO rides(user_id,  ride_code) VALUES (\'{user_id}\', {ride_code})""".format(
                                        user_id=user_obj.id, ride_code=ride_code
    ))
    _connection.commit()


def insert_ride(ride):
    cur = _connection.cursor()
    cur.execute("INSERT INTO rides (user_id, ride_code ,payment ,payment_hash) VALUES (%s, %s, %s, %s)", (
        ride.user_id, ride.ride_code, ride.amount_paid, ride.hash))
    _connection.commit()


def insert_user(user):
    print 'inserting'
    cur = _connection.cursor()
    # b = """INSERT INTO %s (user_id, id_card, last_name, first_name) VALUES (%s, %d, %s, %s)""", (
    #     (rides, user.id, user.government_id, user.last_name, user.first_name))
    # print b
    cur.execute("INSERT INTO user_base (user_id, id_card, last_name, first_name, token) VALUES (%s, %s, %s, %s, %s)", (
        user.id, user.government_id, user.last_name, user.first_name, user.token))
    _connection.commit()


def update_user_token(user_id, token):
    cur = _connection.cursor()
    cur.execute("""UPDATE user_base SET token=\'{token}\' WHERE user_id=\'{user_id}\'""".format(user_id=user_id, token=token))
    _connection.commit()