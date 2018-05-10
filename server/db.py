import psycopg2

from classes import Ride, User, NoSuchUser

url = '192.168.1.20'
dbname = 'lightkavdb'
_connection = psycopg2.connect("dbname='{}' user='postgres' host='{}' password='lightkavwins'".format(dbname, url))


def select_all_users():
    cur = _connection.cursor()
    cur.execute('SELECT * from public.user_base')
    rows = cur.fetchall()
    return [User(*r) for r in rows]


def select_users_by_token(token):
    cur = _connection.cursor()
    cur.execute('SELECT * from public.user_base WHERE token={}'.format(token))
    rows = cur.fetchall()
    if not rows:
        raise NoSuchUser('no user with token {}'.format(token))
    return rows[0]


def select_rides_by_user_token(user_token):
    cur = _connection.cursor()
    user_id = select_users_by_token(user_token)[0]
    cur.execute('SELECT * from public.rides WHERE user_id={}'.format(user_id))
    rows = cur.fetchall()
    return [Ride(*r) for r in rows]


def select_all_rides():
    cur = _connection.cursor()
    cur.execute('SELECT * from public.rides')
    rows = cur.fetchall()
    return [Ride(*r) for r in rows]


def insert_ride(ride):
    cur = _connection.cursor()
    cur.executemany("""INSERT INTO public.rides(user_id,  ride_code  ,payment   ,payment_hash) 
                    VALUES ({user_id}), ({ride_code}), ({payment}), ({payment_hash})""".format(
            user_id=ride.phone_id, ride_code=ride.ride_code, payment=ride.amount_paid, payment_hash=ride.hash
    ))


def insert_user(user):
    cur = _connection.cursor()
    cur.executemany("""INSERT INTO public.user_base(user_id,id_card,last_name,first_name) 
                    VALUES (({user_id}), ({id_card}), ({last_name}), ({first_name}))""".format(
                user_id=user.id, id_card=user.government_id, last_name=user.last_name, first_name=user.first_name
    ))

