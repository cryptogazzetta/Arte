import psycopg2
import sys
import constants

db_params = constants.db_params

def create_connection():
    """ Create a connection to the PostgreSQL database server """
    conn = None
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db_params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print('Connection successful')
    return conn

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

## QUERIES
def create_user(email, artwork_info):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        insert_query = "INSERT INTO USERS (EMAIL, ARTWORK_INFO) VALUES (%s, %s)"
        cursor.execute(insert_query, (email, artwork_info))
        connection.commit()
    finally:
        close_connection(connection, cursor)

def get_user(email):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        select_query = "SELECT * FROM USERS WHERE EMAIL = %s"
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()
        return user
    finally:
        close_connection(connection, cursor)

def update_user(email, artwork_info):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        update_query = "UPDATE USERS SET ARTWORK_INFO = %s WHERE EMAIL = %s"
        cursor.execute(update_query, (artwork_info, email))
        connection.commit()
    finally:
        close_connection(connection, cursor)

def delete_user(email):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        delete_query = "DELETE FROM USERS WHERE EMAIL = %s"
        cursor.execute(delete_query, (email,))
        connection.commit()
    finally:
        close_connection(connection, cursor)