import psycopg2
from config import config
import psycopg2.extras


class Connect:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.params = config()

    def __enter__(self):
        try:
            with psycopg2.connect(**self.params) as self.connection:
                print('connecting to the postgresql database ...')
                self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise
        else:
            return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            print('closing cursor ...')
            self.cursor.close()
        if self.connection is not None:
            print("closing connection... ")
            self.connection.commit()
            self.connection.close()



