CREATE_TABLE_USER = '''
CREATE TABLE IF NOT EXISTS users(
user_id SERIAL PRIMARY KEY ,
username varchar(50) NOT NULL UNIQUE ,
Password varchar(100) NOT NULL,
phone_number varchar(100)) '''

CREATE_TABLE_TICKET = '''
CREATE TABLE IF NOT EXISTS tickets(
ticket_id SERIAL PRIMARY KEY ,
user_id INT NOT NULL ,
type varchar(8) CHECK(type='one-trip' or type='credit'),
balance INT,
 FOREIGN KEY (user_id) REFERENCES users(user_id))'''

CREATE_TABLE_TRIP = '''
CREATE TABLE IF NOT EXISTS trips(
trip_id SERIAL PRIMARY KEY ,
origin varchar(100) ,
destination varchar(100),
departure_time Time,
price decimal(10,5)) '''

CREATE_TABLE_ROLES='''
CREATE TABLE IF NOT EXISTS roles(
role_id serial PRIMARY KEY,
user_type varchar(10) unique ) '''

INSERT_USER = '''INSERT INTO users (username,Password,phone_number,role_id) VALUES (%s,%s,%s,1)'''
INSERT_TICKET = '''INSERT INTO tickets (user_id,type,balance) VALUES (%s,%s,%s)'''
INSERT_TRIP = '''INSERT INTO trips (origin,destination,departure_time,price) VALUES (%s,%s,%s,%s)'''

QUERY_LOGIN = '''SELECT user_id , role_id FROM users WHERE username=%s AND password=%s'''
FIND_TICKET_BY_ID = '''SELECT ticket_id,balance FROM tickets WHERE type='credit' AND user_id=%s'''

# INCREASE_CHARGE_CREDIT = '''UPDATE tickets SET balance=balance+%s
# WHERE ticket_id=%s'''

QUERY_SHOW_TRIPS_FROM_NOW = '''SELECT * FROM trips WHERE departure_time>now()::TIME order by departure_time'''
QUERY_SHOW_TRIPS = '''SELECT * FROM trips  order by departure_time'''

INSERT_TICKET_ONE_TRIP = '''INSERT INTO tickets (user_id,type) VALUES (%s,'one-trip')'''

# DECREASE_CHARGE_CREDIT = '''UPDATE tickets SET balance=balance-%s
# WHERE ticket_id=%s'''

UPDATE_CHARGE_QUERY='''UPDATE tickets SET balance= %s
WHERE ticket_id=%s'''
