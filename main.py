from flask import Flask, render_template, request, session
from flask_restful import Api
from user import register_user_route
from homepage import homepage
from userLogin import login_route
from taskAdd import add_task
from displayTask import delete_task, get_all_tasks
from empDetails import submit_form
from database import connect_to_database, close_database_connection
from logger import configure_data_logger, configure_error_logger

app = Flask(__name__)
api = Api(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = "uday"


# Connect to MySQL database
connection = connect_to_database()

# Configure data and error logging
data_logger = configure_data_logger()
error_logger = configure_error_logger()

# Register routes
app.route('/users', methods=['POST'])(register_user_route)
app.route('/login', methods=['POST'])(login_route)
app.route('/get-username/<int:user_id>', methods=['GET'])(homepage)
app.route('/addtask/', methods=['POST'])(add_task)
app.route('/gettasks', methods=['GET'])(get_all_tasks)
app.route('/deletetask/<int:task_id>/', methods=['DELETE'])(delete_task)
app.route('/submit_form', methods=['POST'])(submit_form)

@app.route('/')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/homePage')
def home_page():
    return render_template('homePage.html')

@app.route('/taskDetails')
def task_details():
    return render_template('taskDetails.html')

@app.route('/empDetails', methods=['GET', 'POST'])
def emp_details():
    if request.method == 'GET':
        # Handle GET request
        # For example, return a template for displaying the form
        return render_template('emp_details.html')
    elif request.method == 'POST':
        # Handle POST request
        # For example, process form data
        return submit_form()

if __name__ == '__main__':
    port = 8080
    app.run(debug=True, port=port)
    # Close the database connection when the application exits
    close_database_connection(connection)
