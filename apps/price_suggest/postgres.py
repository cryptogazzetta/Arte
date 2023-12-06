import streamlit as st
from sqlalchemy import text
import datetime
import logging


# CONNECTION
def create_connection():
    conn = None
    
    print('Connecting to the PostgreSQL database...')
    # conn = psycopg2.connect(**local_db_params)
    # Using streamlit community cloud instead
    conn = st.connection("postgresql", type="sql")

    # except (Exception) as error:
    #     print(error)
    print("Connection successful")
    return conn

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

## PRICE CONSULTATIONS CRUD
def create_consultation(email, artist, medium_type, height, width, year):
    try:
        conn = create_connection()
        with conn.session as session:
            timestamp = datetime.datetime.now()
            insert_query = f"INSERT INTO CONSULTATIONS (email, artist, medium_type, height, width, year, timestamp) VALUES ('{email}', '{artist}', '{medium_type}', {height}, {width}, {year}, '{timestamp}');"
            session.execute(text(insert_query))
            session.commit()
        logging.info('User created')
    except (Exception) as error:
        logging.error(error)

def get_all_consultations():
    try:
        connection = create_connection()
        users = connection.query('SELECT * FROM CONSULTATIONS;')
    except (Exception) as error:
        logging.error('error executing get_all_consultations postgres function:', error)
    return users

def get_consultation(email):
    try:
        connection = create_connection()
        select_query = f"SELECT * FROM CONSULTATIONS WHERE EMAIL = '{email}';"
        user = connection.execute(select_query, (email))
        return user
    except (Exception) as error:
        logging.error('error executing get_user postgres function:', error)
