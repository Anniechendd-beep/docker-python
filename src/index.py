from flask import Flask, request, render_template_string
import pymysql
import os

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user='root',
        password='abc123',
        database='my_db',
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description', '')
            cursor.execute('INSERT INTO todos (title, description) VALUES (%s, %s)', (title, description))
            conn.commit()
        
        cursor.execute('SELECT * FROM todos ORDER BY id DESC')
        todos = cursor.fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo List</title>
    </head>
    <body>
        <h1>Todo List</h1>
        <form method="post">
            <input type="text" name="title" placeholder="Title" required>
            <input type="text" name="description" placeholder="Description">
            <button type="submit">Add Todo</button>
        </form>
        <ul>
        {% for todo in todos %}
            <li>
                <strong>{{ todo.title }}</strong>: {{ todo.description }}
                <form method="post" action="/toggle/{{ todo.id }}" style="display:inline;">
                    <button type="submit">{{ 'Mark Complete' if not todo.completed else 'Mark Incomplete' }}</button>
                </form>
                <form method="post" action="/delete/{{ todo.id }}" style="display:inline;">
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html, todos=todos)

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE todos SET completed = NOT completed WHERE id = %s', (todo_id,))
        conn.commit()
    conn.close()
    return '', 204

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM todos WHERE id = %s', (todo_id,))
        conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)