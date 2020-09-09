# Import Flask modules
from flask import Flask, jsonify, abort, request
#from flask library import MySQL
from flaskext.mysql import MySQL

#api = Api(app)

# Create an object named app
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'to-do.cdjqc1ck02ug.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'to_do'
mysql = MySQL()
mysql.init_app(app)
connection=mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

mysql.connection.cursor()



# Write a function named `init_to-do_db` which initializes the to-do db
# Create tasks table within sqlite db and populate with sample data
# Execute the code below only once.


"""
    CREATE TABLE tasks(
    task_id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    is_done BOOLEAN NOT NULL DEFAULT 0 CHECK(is_done IN(0,1)));
"""
#data = 
"""
    INSERT INTO tasks (title, description, is_done)
    VALUES
        ("Study AWS", "AWS RDS", 1 ),
        ("Study SQL", "MySQL", 0),
        ("Study Flask", "Install Flask and write a python Rest API program", 0);
"""

# Write a function named `get_all_tasks` which gets all tasks from the tasks table in the db,
# and return result as list of dictionary
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': True or False} ]`.


def get_all_tasks():
    query = """
    SELECT * FROM tasks;
    """
    #result = mysql.session.execute(query)
    cursor.execute(query)
    result = cursor.fetchall()

    tasks = [{'task_id': row[0], 'title':row[1], 'description':row[2],
              'is_done': bool(row[3])} for row in result]
    return tasks


# Write a function named `find_task` which finds task using task_id from the tasks table in the db,
# and return result as list of dictionary
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': 'Yes' or 'No'} ]`.
def find_task(id):
    query = f"""
    SELECT * FROM tasks WHERE task_id={id};
    """
    cursor.execute(query)
    result = cursor.fetchone()
    
    row = result.first()
    task = None
    if row is not None:
        task = {'task_id': row[0], 'title': row[1],
                'description': row[2], 'is_done': bool(row[3])}
    return task

# Write a function named `insert_task` which inserts task into the tasks table in the db,
# and return the newly added task as dictionary
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': 'Yes' or 'No'} ]`.
def insert_task(title, description):
    insert = f"""
    INSERT INTO tasks (title, description)
    VALUES ('{title}', '{description}');
    """
    result = mysql.session.execute(insert)
    mysql.session.commit()

    query = f"""
    SELECT * FROM tasks WHERE task_id={result.lastrowid};
    """
    row = mysql.session.execute(query).first()

    return {'task_id':row[0], 'title':row[1], 'description':row[2], 'is_done': bool(row[3])}

# Write a function named `change_task` which updates task into the tasks table in the db,
# and return updated added task as dictionary
# `[{'task_id': 1, 'title':'XXXX', 'description': 'XXXXXX', 'is_done': 'Yes' or 'No'} ]`.
def change_task(task):
    update = f"""
    UPDATE tasks
    SET title='{task['title']}', description = '{task['description']}', is_done = {task['is_done']}
    WHERE task_id= {task['task_id']};
    """

    result = mysql.session.execute(update)
    mysql.session.commit()

    query = f"""
    SELECT * FROM tasks WHERE task_id={task['task_id']};
    """
    row = mysql.session.execute(query).first()
    return {'task_id':row[0], 'title':row[1], 'description':row[2], 'is_done': bool(row[3])}

# Write a function named `remove_task` which removes task from the tasks table in the db,
# and returns True if successfully deleted or False.
def remove_task(task):
    delete = f"""
    DELETE FROM tasks
    WHERE task_id= {task['task_id']};
    """

    result = mysql.session.execute(delete)
    mysql.session.commit()

    query = f"""
    SELECT * FROM tasks WHERE task_id={task['task_id']};
    """
    row = db.session.execute(query).first()

    return True if row is None else False


# Write a function named `home` which returns 'Welcome to the Callahan's to-do API Service',
# and assign to the static route of ('/')
@app.route('/')
def home():
    return "Welcome to Baur's Project 3 To-Do API Service"

# Write a function named `get_tasks` which returns all tasks in JSON format for `GET`,
# and assign to the static route of ('/tasks')
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': get_all_tasks()})

# Write a function named `get_task` which returns the task with given task_id in JSON format for `GET`,
# and assign to the static route of ('/tasks/<int:task_id>')
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    return jsonify({'task found':task})

# Write a function named `add_task` which adds new task using `POST` methods,
# and assign to the static route of ('/tasks')
@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    return jsonify({'newly added task':insert_task(request.json['title'], request.json.get('description', ''))}), 201

# Write a function named `update_task` which updates an existing task using `PUT` method,
# and assign to the static route of ('/tasks/<int:task_id>')
@app.route('/tasks/<int:task_id>', methods=['PUT'] )
def update_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    if not request.json:
        abort(400)
    task['title']=request.json.get('title', task['title'])
    task['description']=request.json.get('description', task['description'])
    task['is_done']=int(request.json.get('is_done', int(task['is_done'])))
    return jsonify({'updated task': change_task(task)})

# Write a function named `delete_task` which updates an existing task using `DELETE` method,
# and assign to the static route of ('/tasks/<int:task_id>')
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    return jsonify({'result':remove_task(task)})

# Add a statement to run the Flask application which can be reached from any host on port 5000.
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)