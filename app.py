import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g

app = Flask(__name__)

app.secret_key = 'id_generator' 
DATABASE = 'idcard_generator.db'

# --- SQLite Database Functions ---

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database schema and populates sample student data."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # 1. User/Login Table 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. ID Card Data Table 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS id_cards (
                card_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                id_number TEXT NOT NULL,
                title TEXT,
                department TEXT,
                valid_until TEXT,
                photo_url TEXT,
                template_key TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        
        # Sample Student Logins (usernames: 'student1' to 'student5', password: 'pass')
        sample_users = [
            ('student1', 'pass'),
            ('student2', 'pass'),
            ('student3', 'pass'),
            ('student4', 'pass'),
            ('student5', 'pass')
        ]
        
        # Insert sample users if they don't exist
        for username, password in sample_users:
            try:
               
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            except sqlite3.IntegrityError:
                # User already exists
                pass

        db.commit()

# --- Routes ---

@app.route('/')
def index():
    """Render the main landing page."""
    return render_template('index.html')


# --- Login Route  ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login and redirects upon success."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        # Find user by username and password
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?', (username, password)
        ).fetchone()

        if user:
            # Successful login
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('generator'))
        else:
            # Failed login
            return render_template('login.html', error='Invalid credentials. Please try again or Sign Up.')

    return render_template('login.html')

# --- Signup Route ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user registration and saves new user to the database."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        try:
           
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            db.commit()
            # Redirect to login after successful signup
            return redirect(url_for('login', message='Account created successfully! Please log in.'))
        except sqlite3.IntegrityError:
            # Handle case where username already exists
            return render_template('signup.html', error='Username already taken. Please choose another.')
        except Exception as e:
            return render_template('signup.html', error=f'An error occurred: {e}')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Logs the user out."""
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/generator', methods=['GET'])
def generator():
    """Serves the main ID card generator page, requires login."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    
    return render_template('generator.html', username=session['username'])


@app.route('/save_data', methods=['POST'])
def save_data():
    """Saves the ID card data to the SQLite database ."""
    if not session.get('logged_in'):
        return {'status': 'error', 'message': 'Authentication required'}, 401

    try:
        data = request.json
        user_id = session['user_id']
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("""
            INSERT INTO id_cards (user_id, name, id_number, title, department, valid_until, photo_url, template_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data.get('name'),
            data.get('id'),
            data.get('title'),
            data.get('dept'),
            data.get('valid'),
            data.get('photoUrl'),
            data.get('templateKey') 
        ))
        
        db.commit()
        
        return {'status': 'success', 'message': 'Data saved successfully!', 'card_id': cursor.lastrowid}
    
    except Exception as e:
        print(f"Database Save Error: {e}")
        return {'status': 'error', 'message': f'Internal server error: {e}'}, 500

# --- User List  ---
@app.route('/users')
def list_users():
    """Fetches all registered users from the database and displays them in a table."""
 
    
    db = get_db()
    users = db.execute('SELECT id, username, created_at FROM users ORDER BY id DESC').fetchall()
    
    return render_template('user_list.html', users=users)


if __name__ == '__main__':
    init_db() 
    app.run(debug=True)