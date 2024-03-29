import os
import mysql.connector

from dotenv import load_dotenv
load_dotenv('auth.env')

class Database(object):

    def __init__(self):

        password = os.getenv('MYSQL_PASSWORD')
        conn = mysql.connector.connect(user='predictor', password=password, host='localhost', database='predictor')

        self.cnx = conn

    # Connect DB
    def connect_to_database(self):
        return self.cnx

    # Disconnect DB
    def disconnect_database(self):
        self.cnx.close()

    def create_cursor(self):
        return self.cnx.cursor(dictionary=True)

    def commit(self):
        self.cnx.commit()

    def close_cursor(self):
        cursor = self.create_cursor()
        cursor.close()

