from flask import Flask, request, jsonify, session
from database import connect_to_database  
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/deletetask/<int:task_id>/', methods=['DELETE'])
def delete_task(task_id):
    with connect_to_database() as connection:
        cursor = connection.cursor()
        user_id = session.get('user_id')
        sql_query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
        cursor.execute(sql_query, (task_id, user_id))
        connection.commit()
    return jsonify({'message': 'Task deleted successfully'})


@app.route('/gettasks', methods=['GET'])
def get_all_tasks():
    with connect_to_database() as connection:
        cursor = connection.cursor()
        user_id = session.get('user_id')
        sql_query = "SELECT id, title, description, due_date, priority FROM tasks WHERE user_id = %s"
        cursor.execute(sql_query, (user_id,))
        tasks = cursor.fetchall()

    task_list = []
    for task in tasks:
        task_details = {
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'dueDate': task[3].strftime('%Y-%m-%d'),
            'priority': task[4]
        }
        task_list.append(task_details)

    return jsonify({'tasks': task_list})


if __name__ == '__main__':
    app.run(debug=True)
