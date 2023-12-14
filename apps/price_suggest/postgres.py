import datetime
import logging
import psycopg2
import constants

## CONNECTION
local_db_params = constants.local_db_params

def create_connection():
    connection = None
    cursor = None
    try:
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**local_db_params)
        cursor = connection.cursor()
    except (Exception) as error:
        print(error)
    print("Connection successful")
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

## POSTGRES FUNCTIONS
def get_all_consultations():
    try:
        connection, cursor = create_connection()
        
        cursor.execute('SELECT * FROM CONSULTATIONS;')
        users = cursor.fetchall()
        
        close_connection(connection, cursor)
    except (Exception) as error:
        logging.error('error executing get_all_consultations postgres function:', error)
    return users

def create_consultation(email, artist, medium_type, height, width, year):
    # try:
    connection, cursor = create_connection()
    timestamp = datetime.datetime.now()
    insert_query = f"INSERT INTO CONSULTATIONS (email, artist, medium_type, height, width, year, timestamp) VALUES ('{email}', '{artist}', '{medium_type}', {height}, {width}, {year}, '{timestamp}');"
    cursor.execute(insert_query)
    connection.commit()
    close_connection(connection, cursor)
    logging.info('User created')
    # except (Exception) as error:
    #     logging.error(error)