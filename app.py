import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'todoapp')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, task FROM todos ORDER BY created_at DESC')
    todos = cur.fetchall()
    cur.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task and task.strip():
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO todos (task) VALUES (%s)', [task.strip()])
        mysql.connection.commit()
        todo_id = cur.lastrowid
        cur.close()
        return jsonify({'success': True, 'id': todo_id, 'task': task.strip()})
    return jsonify({'success': False, 'error': 'Task cannot be empty'})

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s', [todo_id])
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    
    if rows_affected > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Todo not found'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)