from flask import Flask, request, jsonify, session, redirect, url_for, render_template,session
from database import connect_to_database, close_database_connection, Error
from userLogin import login_route

app = Flask(__name__)


@app.route('/empDetails', methods=['GET','POST'])
def submit_form():
    user_id = session.get('user_id')
    if not user_id:
            return "User not logged in", 403
    if request.method == 'POST':
        data = request.json 
        
        # Extracting data from JSON
        full_name = data.get('full_name')
        employee_id = data.get('employee_id')
        gender = data.get('gender')
        dob = data.get('dob')
        nationality = data.get('nationality')
        address = data.get('address')
        phone = data.get('phone')
        email = data.get('email')
        job_title = data.get('job_title')
        department =  data.get('department')
        date_of_hire = data.get('date_of_hire')
        employment_status = data.get('employment_status')
        reporting_manager = data.get('reporting_manager')
        salary = data.get('salary')
        pay_frequency = data.get('pay_frequency')
        bonus = data.get('bonus')
        benefits = data.get('benefits')
        work_location = data.get('work_location')
        
        # Check if user is logged in
        if user_id:
            try:
                # Connect to the database
                db_connection = connect_to_database()
                cursor = db_connection.cursor()
                select_query = """
                SELECT * FROM employees WHERE user_id = %s
            """
                cursor.execute(select_query, (user_id,))
                employee_details = cursor.fetchall()

                # Insert personal information into the employees table
                employee_insert_query = """
                    INSERT INTO employees (user_id, full_name, 
                    employee_id, gender, dob, nationality)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(employee_insert_query, (
                    user_id, full_name, employee_id, gender, dob, nationality
                ))

                # Insert contact information into the contacts table
                contact_insert_query = """
                    INSERT INTO contacts (user_id, address, phone, email)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(contact_insert_query, (
                    user_id, address, phone, email
                ))

                # Insert employment details into the employment table
                employment_insert_query = """
                    INSERT INTO employment (user_id, job_title, department, date_of_hire, employment_status, reporting_manager, salary, pay_frequency, bonus, benefits, work_location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(employment_insert_query, (
                    user_id, job_title, department, date_of_hire,
                    employment_status, reporting_manager,
                    salary, pay_frequency, bonus,
                    benefits, work_location
                ))

                # Commit the transaction
                db_connection.commit()

                # Close cursor and database connection
                cursor.close()
                close_database_connection(db_connection)

                # Redirect to the home page or return a success message
                return jsonify({"message": "Form data submitted successfully"})

            except Error as e:
                # Rollback in case of any error
                db_connection.rollback()
                # Log error and return an error message
                app.logger.error("Error inserting form data: %s", str(e))
                return "An error occurred while processing your request."

        return "Form submitted successfully"  # Or return a JSON response

    return "Invalid request method"

@app.route('/viewEmployeeDetails')
def view_employee_details():
    user_id = session.get('user_id')
    if user_id:
        try:
            # Connect to the database
            db_connection = connect_to_database()
            cursor = db_connection.cursor()

            # Query employee details based on user ID
            select_query = """
                SELECT * FROM employees WHERE user_id = %s
            """
            cursor.execute(select_query, (user_id,))
            employee_details = cursor.fetchall()

            # Close cursor and database connection
            cursor.close()
            close_database_connection(db_connection)

            # Return employee details
            return jsonify(employee_details)

        except Error as e:
            # Log error and return None or an empty list
            app.logger.error("Error fetching employee details: %s", str(e))

    return jsonify([])  # Return empty list if user is not logged in or if there's an error


if __name__ == '__main__':
    app.run(debug=True)
