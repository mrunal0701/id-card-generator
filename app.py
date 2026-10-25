import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
import json

app = Flask(__name__)

app.secret_key = 'resume_builder_key' 
DATABASE = 'resume_builder.db'

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
    """Initializes the database schema and populates sample user data."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # 1. User/Login Table (Unchanged)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. RESUME Data Table (NEW SCHEMA)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                resume_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                title TEXT,
                objective TEXT,
                contact_details TEXT, -- JSON string for email, phone, linkedin
                education TEXT,      -- JSON string of education entries
                work_experience TEXT, -- JSON string of work entries
                skills TEXT,          -- Comma-separated or JSON list
                projects TEXT,        -- JSON string of project entries
                template_key TEXT,
                photo_url TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)
        
        # Sample Users (to ensure the app runs initially)
        sample_users = [
            ('resumer1', 'pass'),
            ('resumer2', 'pass'),
        ]
        
        for username, password in sample_users:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            except sqlite3.IntegrityError:
                pass

        db.commit()

# --- Routes (Login/Signup/Logout remain the same) ---

@app.route('/')
def index():
    return render_template('index.html')


# --- Login Route ---
# (Keep your existing login function here)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?', (username, password)
        ).fetchone()

        if user:
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('generator'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again or Sign Up.')

    return render_template('login.html')

# --- Signup Route ---
# (Keep your existing signup function here)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
            return redirect(url_for('login', message='Account created successfully! Please log in.'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error='Username already taken. Please choose another.')
        except Exception as e:
            return render_template('signup.html', error=f'An error occurred: {e}')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/generator', methods=['GET'])
def generator():
    """Serves the main Resume Builder page, requires login."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('generator.html', username=session['username'])


@app.route('/save_data', methods=['POST'])
def save_data():
    """Saves the comprehensive resume data to the SQLite database."""
    if not session.get('logged_in'):
        return {'status': 'error', 'message': 'Authentication required'}, 401

    try:
        data = request.json
        user_id = session['user_id']
        
        db = get_db()
        cursor = db.cursor()
        
        # Prepare data for insertion (assuming complex fields are JSON strings from frontend)
        # Note: In a real app, validation and better JSON handling is needed.
        
        cursor.execute("""
            INSERT INTO resumes (user_id, name, title, objective, contact_details, education, work_experience, skills, projects, template_key, photo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            data.get('name'),
            data.get('title'),
            data.get('objective'),
            json.dumps(data.get('contact', {})),
            json.dumps(data.get('education', [])),
            json.dumps(data.get('work', [])),
            data.get('skills'), # Simple string for now
            json.dumps(data.get('projects', [])),
            data.get('templateKey'),
            data.get('photoUrl')
        ))
        
        db.commit()
        
        return {'status': 'success', 'message': 'Resume data saved successfully!', 'resume_id': cursor.lastrowid}
    
    except Exception as e:
        print(f"Database Save Error: {e}")
        return {'status': 'error', 'message': f'Internal server error: {e}'}, 500


@app.route('/recommend', methods=['POST'])
def recommend():
    """Provides recommendations based on the selected domain/title."""
    data = request.json
    title = data.get('title', '').lower()

    recommendations = {
        'software engineer': {
            'objective': 'Seeking a challenging role in software development to utilize my skills in modern frameworks and contribute to scalable solutions.',
            'skills': 'Python, JavaScript, React, Node.js, REST APIs, SQL/NoSQL, Git, AWS/Azure, Agile/Scrum.',
            'tip': 'For a Software Engineer, quantify your project impact (e.g., "reduced latency by 20%"). Focus on **Problem, Action, Result (PAR)** in your work experience.'
        },
        'data scientist': {
            'objective': 'Highly analytical Data Scientist passionate about extracting insights from complex datasets to drive data-informed decision-making.',
            'skills': 'Python (Pandas, NumPy, Scikit-learn), R, SQL, Machine Learning, Deep Learning, Statistical Modeling, Data Visualization (Matplotlib, Tableau).',
            'tip': 'For a Data Scientist, highlight specific **models, algorithms, and accuracy metrics** you achieved. Showcase project results clearly.'
        },
        'marketing specialist': {
            'objective': 'Creative and results-driven Marketing Specialist aiming to boost brand awareness and increase conversion rates through strategic digital campaigns.',
            'skills': 'SEO/SEM, Google Analytics, Social Media Marketing (SMM), Content Strategy, Email Marketing, Hubspot/Salesforce, A/B Testing.',
            'tip': 'For Marketing, always use **metrics and percentages**. (e.g., "Increased organic traffic by 45% in 6 months").'
        }
    }
    
    # Simple matching logic
    for key, rec in recommendations.items():
        if key in title:
            return rec
            
    # Default recommendation
    return {
        'objective': 'Dedicated professional seeking an opportunity to apply my skills and contribute to a successful organization.',
        'skills': 'Communication, Teamwork, Problem-Solving, Time Management, Adaptability.',
        'tip': 'Ensure your resume is **one page** if you have under 10 years of experience. Use **bullet points** and a **clean, readable font**.'
    }


# --- User List ---
# (Keep your existing list_users function here)

@app.route('/users')
def list_users():
    db = get_db()
    users = db.execute('SELECT id, username, created_at FROM users ORDER BY id DESC').fetchall()
    return render_template('user_list.html', users=users)


if __name__ == '__main__':
    init_db() 
    app.run(debug=True)