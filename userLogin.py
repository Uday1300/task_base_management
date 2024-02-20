from flask import Flask, request, jsonify, session
from flask_session import Session
from database import connect_to_database, close_database_connection, Error, create_table_query
import bcrypt
from logger import configure_data_logger, configure_error_logger
from mysql.connector import Error as MySQLError
import secrets
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/login', methods=['POST'])
def login_route():
    cursor = None

    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        with connect_to_database() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM userModel WHERE email = %s", (email,))
            user = cursor.fetchone()

        if user is None:
            return {"error": "User not found"}, 404

        # Check if the provided password matches the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            # Store user information in the session dictionary
            session['user_id'] = user[0]
            session['user_email'] = user[2]

            return {"status": "success", "message": f"Login successful {email}"}, 200
        else:
            return {"error": "Incorrect password"}, 401

    except MySQLError as e:
        # Log specific database errors
        configure_error_logger.error("Database error during login: %s", str(e), exc_info=True)
        return {"error": "Database error occurred during login"}, 500
    except Exception as e:
        # Log unexpected errors
        configure_error_logger.error("Unexpected error during login: %s", str(e), exc_info=True)
        return {"error": "Unexpected error occurred during login"}, 500

    finally:
        # Close the database cursor
        if cursor is not None:
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
