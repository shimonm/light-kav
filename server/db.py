import psycopg2

from classes import Ride, User

url = '192.168.1.20'
dbname = 'lightkavdb'
_connection = psycopg2.connect("dbname='{}' user='postgres' host='{}' password='lightkavwins'".format(dbname, url))


def select_all_users():
    cur = _connection.cursor()
    cur.execute('SELECT * from public.user_base')
    rows = cur.fetchall()
    return [User(*r) for r in rows]


def select_all_rides():
    cur = _connection.cursor()
    cur.execute('SELECT * from public.rides')
    rows = cur.fetchall()
    return [Ride(*r) for r in rows]


def insert_ride():
    cur = _connection.cursor()
    cur.executemany("""INSERT INTO public.rides(user_id,ride_code,payment,payment_hash) 
    VALUES (%(first_name)s, %(last_name)s)""", namedict)
    cur.execute('INSERT INTO public.rides ')


def insert_user():
    cur = _connection.cursor()
    cur.executemany("""INSERT INTO public.user_base(user_id,id_card,last_name,first_name) 
    VALUES (%(first_name)s, %(last_name)s)""", namedict)
    cur.execute('INSERT INTO public.rides ')

