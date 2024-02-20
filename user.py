from flask import Flask, request, abort ,jsonify
from datetime import datetime
import bcrypt
import re
from database import connect_to_database, close_database_connection, Error, create_table_query
from logger import configure_data_logger, configure_error_logger
import time
import json

app = Flask(__name__)

connection = connect_to_database()
data_logger = configure_data_logger()
error_logger = configure_error_logger()

user_tabel = 'userModel' 
user_data = {
    "name": "",
    "email": " ",
    "password": " ",
    "time": ""
}

def is_valid_email(email):
    # Define a regular expression for validating email addresses
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Return True if the email matches the regular expression, else return False
    return re.match(email_regex, email) is not None

def user_exists(email, connection):
    # Check if a user with the provided email already exists in the database
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM userModel WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    return existing_user is not None


def validate_user_data(user_data, hashed_password, connection, data_logger, error_logger):
    # Create a database cursor
    cursor = connection.cursor()
    try:
        if not user_data or not isinstance(user_data, dict):
            error_logger.error("Invalid user data: %s", user_data)
            return {"error": "Invalid user data"}

        # Parse the input time and calculate the time difference
        input_time = time.strptime(user_data['time'], "%H:%M:%S")
        current_time = time.localtime()
        time_difference = (
            current_time.tm_hour * 3600 + current_time.tm_min * 60 + current_time.tm_sec -
            input_time.tm_hour * 3600 - input_time.tm_min * 60 - input_time.tm_sec)

        # Log information about the current time, input time, and time difference
        data_logger.debug("Current Time: %s", current_time)
        data_logger.debug("Input Time: %s", input_time)
        data_logger.debug("Time Difference: %s", time_difference)

        # Check if the time difference is within 30 seconds
        if time_difference <= 30:
            # If within 30 seconds, insert user data into the database
            cursor.execute(
                "INSERT INTO userModel(name, email, password, created_at) VALUES (%s, %s, %s, %s)",
                (user_data.get('name'), user_data.get('email'), hashed_password, time.strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
            return {"message": "User data validated successfully"}

        else:
            # If time difference exceeds 30 seconds, log an error and return an error response
            error_logger.error("Time difference exceeds 30 seconds")
            return {"error": "Time difference exceeds 30 seconds"}

    except Exception as e:
        # Log validation error and return an error response
        error_logger.error("Validation error: %s", str(e), exc_info=True)
        return {"error": f"Validation error: {str(e)}"}

    finally:
        # Close the database cursor in the finally block
        cursor.close()

@app.route('/users', methods=['POST'])
def register_user_route():
    try:
        cursor = connection.cursor()
        # Extract JSON data from the request
        request_data = request.get_json()

        # Ensure that the required fields are present in the request data
        required_fields = ['name', 'email', 'password', 'time']
        if not all(field in request_data for field in required_fields):
            return {"error": "Missing required fields"}, 400

        # Assign data to the user_data dictionary
        user_data["name"] = request_data.get("name")
        user_data["email"] = request_data.get("email")
        user_data["password"] = request_data.get("password")
        user_data["time"] = request_data.get("time")

        if not user_data['password']:
            return {"error": "Password cannot be empty"}, 400
        # Hash the user's password using bcrypt
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

        # Validate the email format
        if not is_valid_email(user_data['email']):
            print(user_data)
            return {"error": "Please Enter a valid email"}, 400
        
        
        cursor.execute(f"SHOW TABLES LIKE '{user_tabel}'")
        table_exists = cursor.fetchone()
        print(table_exists)
        if not table_exists:
            cursor.execute(create_table_query)

        # Return an error if a user with the given user_id or email already exists, along with a 400 Bad Request status.
        if user_exists(user_data['email'], connection):
            return {"error": "User with the provided user_id or email already exists"}, 400

        # Validate user data using a custom method
        validation_result = validate_user_data(user_data, hashed_password, connection, data_logger, error_logger)


        # Check if there was a validation error
        if validation_result and "error" in validation_result:
            return validation_result, 400

        return {"message": "User data validated successfully"}, 200

    except Exception as e:
        # Log unexpected errors
        error_logger.error("Unexpected error: %s", str(e), exc_info=True)
        return {"error": "Unexpected error occurred"}, 500





