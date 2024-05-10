import queries as q
import faker
import database as db
import random

with db.Connect() as cursor:
    cursor.execute(q.CREATE_TABLE_USER)
    cursor.execute(q.CREATE_TABLE_TICKET)
    cursor.execute(q.CREATE_TABLE_TRIP)

    fake = faker.Faker()
    user_qty = 5
    trip_qty = 10
    ticket_qty = 10
    values = []
    for _ in range(user_qty):
        username = fake.user_name()
        password = fake.password()
        phone_number = fake.phone_number()
        values.append([username, password, phone_number])

    cursor.executemany(q.INSERT_USER, values)

    # ______________________________________________
    type_ticket_valid = ["one-trip", "credit"]
    values = []
    for _ in range(ticket_qty):
        user_id = random.randint(1, user_qty)
        type_ticket = random.choice(type_ticket_valid)
        balance = random.randint(1, 10)
        values.append([user_id, type_ticket, balance])  # [[()]]

    cursor.executemany(q.INSERT_TICKER, values)

    values = []
    for _ in range(trip_qty):
        origin = fake.city()
        destination = fake.city()
        departure_time = fake.time()
        price = random.randint(100, 800)
        values.append([origin, destination, departure_time, price])  # [[()]]

    cursor.executemany(q.INSERT_TRIP, values)
