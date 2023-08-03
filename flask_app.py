from flask import Flask, render_template, request
import psycopg2
import os
from get_pass_from_vault import get_pass_vault
app = Flask(__name__)

def create_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            port=os.environ.get('DB_PORT'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        return conn

    except psycopg2.OperationalError as e:
        print(f"Error: {e}")
        return None
    

if get_pass_vault() == True:
    '''
    True when function from get_pass_from_vault.py will connect to Vault and get sercret
    '''
    conn = create_db_connection()
    if conn is not None:
            
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
            message ="Could not connect to database"
            return render_template('error.html', message=message)


else:
    @app.route('/', methods=['GET'])
    def index():
        message ="HCP Vault doesn't work - did not return password. I think, you should first run ansible playbook - playbook-todoapp"
        return render_template('error.html', message=message)
    
if __name__ == '__main__':
    app.run(debug=True)
