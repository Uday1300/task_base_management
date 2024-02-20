# database.py
import mysql.connector
from mysql.connector import Error

create_table_query = '''
CREATE TABLE IF NOT EXISTS userModel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL
);
'''

def create_user_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("User table created successfully.")
    except Error as e:
        print("Error creating user table: ", e)


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='userRegistration',
            user='root',
            password='root@123',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

        # Create the user table if it doesn't exist
        create_user_table(connection)

        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


def close_database_connection(connection):
    if connection.is_connected():
        connection.close()
