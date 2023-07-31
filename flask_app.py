from flask import Flask, render_template, request
import psycopg2
import os
from get_pass_from_vault import get_pass_vault
app = Flask(__name__)

# Get PostgreSQL connection details from environment variables
if get_pass_vault() == True:
        # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Create a table to store the ToDo items
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            task = request.form['task']
            cur.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
            conn.commit()
        
        cur.execute('SELECT * FROM todos')
        todos = cur.fetchall()
        
        return render_template('index.html', todos=todos)


else:
    @app.route('/', methods=['GET'])
    def index():
        return render_template('error.html')
    
if __name__ == '__main__':
    app.run(debug=True)

