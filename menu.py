import database as db
import queries as q
from prettytable import PrettyTable, from_db_cursor


def menu_main():
    while True:
        menu = "1:Login \n2:register\n3:quit\n"
        print(menu)
        choice = input("Enter your choice? ")
        if choice == "1":
            username = input('Enter username:')
            password = input('Enter password:')
            msg, user_id = login(username, password)
            print(msg)
            if msg == 'username or password is invalid':
                continue
            menu_user(user_id)



        elif choice == "2":
            username = input('Enter username:')
            password = input('Enter password:')
            phone_number = input('Enter phone_number:')
            msg = register(username, password, phone_number)
            print(msg)
        elif choice == "3":
            pass
        else:
            print('Ivalid choice')


def menu_user(user_id):
    while True:
        menu = "1:charge_ticket\n2:choose_trip\n3:quit\n"
        print(menu)
        choice = input("Enter your choice? ")
        if choice == "1":
            with db.Connect() as cursor:
                ticket = has_ticket_credit(user_id, cursor)
                if ticket:
                    charge = get_charge()
                    msg = change_charge_ticket_credit(ticket, cursor, charge)
                else:
                    msg = create_ticket_credit(user_id, cursor)
                print(msg)

                # msg = charge_ticket(user_id)
                # print(msg)

        elif choice == "2":
            with db.Connect() as cursor:
                all_trips = show_trips(cursor)
                trip_id = input("Enter your trip_id: ")
                price = 0
                for trip in all_trips:
                    print('*' * 20, trip['trip_id'])
                    if trip_id == str(trip['trip_id']):
                        price = trip['price']
                        break
                print('*' * 20, price)

                choice = input("trip_type\n1:one_trip\n2:credit ?")
                if choice == "1":
                    msg = create_ticket_one_trip(user_id, cursor)
                    print(msg)
                elif choice == "2":
                    if ticket := has_ticket_credit(user_id, cursor):
                        while True:
                            charge = get_charge()
                            msg = change_charge_ticket_credit(ticket, cursor, -charge)
                            if msg == "Not enough credit":
                                print(msg)
                                print("Increase your charge stupid!")
                                charge = get_charge()
                                msg = change_charge_ticket_credit(ticket, cursor, charge)
                                print(msg)
                                continue
                            break


        elif choice == "3":
            pass
        else:
            print('Ivalid choice')


def has_ticket_credit(user_id, cursor):
    cursor.execute(q.FIND_TICKET_BY_ID, (user_id,))
    ticket = cursor.fetchone()
    if ticket:
        print("ticket_id:", ticket[0], "\tbalance:", ticket[1])
        return ticket
    else:
        print("You dont have ticket")


def get_charge():
    while True:
        charge = input("How much?(int) ")
        try:
            charge = int(charge)
        except ValueError:
            print(f"it's invalid type {charge}")
        else:
            return charge


def increase_charge_ticket_credit(ticket, cursor):
    ticket_id = ticket[0]
    balance = ticket[1]
    while True:
        charge = input("How much balance should it have?(int) ")
        try:
            charge = int(charge)
        except ValueError:
            print(f"it's invalid type {charge}")
        else:
            break
    cursor.execute(q.INCREASE_CHARGE_CREDIT, (charge, ticket_id))
    return f"Ticket {ticket_id} was charged {charge} total is {charge + balance}"


def change_charge_ticket_credit(ticket, cursor, charge):
    ticket_id = ticket[0]
    balance = ticket[1]
    result = balance + charge
    if result >= 0:
        cursor.execute(q.UPDATE_CHARGE_QUERY, (result, ticket_id))
        return f"Ticket {ticket_id} was charged {charge} total is {result}"
    else:
        return "Not enough credit"


def create_ticket_credit(user_id, cursor):
    answer = input("You dont have any credit ticket! Do you want ticket?(y/n) ")
    if answer == "y":
        while True:
            charge = input("How much balance should it have?(int) ")
            try:
                charge = int(charge)
            except ValueError:
                print(f"it's invalid type {charge}")
            else:
                break
        cursor.execute(q.INSERT_TICKET, (user_id, "credit", charge))
        return f"new ticket was created and charged {charge}"
    return "Cancel"


def create_ticket_one_trip(user_id, cursor):
    cursor.execute(q.INSERT_TICKET_ONE_TRIP, (user_id,))
    return f"ur ticket has been added"


def show_trips(cursor):
    cursor.execute(q.QUERY_SHOW_TRIPS)
    # result = from_db_cursor(cursor)

    column_names = [desc[0] for desc in cursor.description]
    all_trips = cursor.fetchall()
    result = PrettyTable(column_names)
    for trip in all_trips:
        result.add_row(trip)

    print(result)
    return all_trips


def register(username, password, phone_number):
    with db.Connect() as cursor:
        cursor.execute(q.INSERT_USER, (username, password, phone_number))
    return 'Successful register'


def login(username, password):
    with db.Connect() as cursor:
        cursor.execute(q.QUERY_LOGIN, (username, password))
        user = cursor.fetchone()
        user_id = None
        if user:
            user_id = user[0]
            return f'welcome {username}', user_id
        return 'username or password is invalid', user_id


if __name__ == '__main__':
    menu_main()
