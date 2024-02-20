# Your Flask backend code
from flask import Flask, request, jsonify, session
from database import connect_to_database 
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

def getUsername(user_id, user_email):
    with connect_to_database() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM userModel WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if user is None:
            return {"error": "User not found"}, 404
        else:
            return {"message": f", {user[0]}"}

@app.route('/get-username/', methods=['GET'])
def homepage(user_id):
    user_id = session.get('user_id') 
    user_email = session.get('user_email') 
    response = getUsername(user_id, user_email)
    return jsonify(response)
