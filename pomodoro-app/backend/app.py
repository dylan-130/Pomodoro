from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
CORS(app, supports_credentials=True, origins=['*'])

# Database setup
def init_db():
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Timer sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS timer_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_type TEXT NOT NULL, -- 'work' or 'break'
        duration INTEGER NOT NULL, -- in minutes
        completed BOOLEAN DEFAULT FALSE,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Timetables table
    c.execute('''CREATE TABLE IF NOT EXISTS timetables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Timetable entries table
    c.execute('''CREATE TABLE IF NOT EXISTS timetable_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timetable_id INTEGER NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        subject TEXT NOT NULL,
        is_break BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (timetable_id) REFERENCES timetables (id)
    )''')
    
    conn.commit()
    conn.close()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Database helper
def get_db():
    conn = sqlite3.connect('pomodoro.db')
    conn.row_factory = sqlite3.Row
    return conn

# Test endpoint
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is working!'}), 200

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    print("DEBUG: Registration endpoint called")
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    print(f"DEBUG: Received data - username: {username}, email: {email}")
    
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    print("DEBUG: About to connect to database")
    conn = get_db()
    try:
        print("DEBUG: Checking if user exists")
        # Check if user exists
        existing_user = conn.execute(
            'SELECT id FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()
        
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        print("DEBUG: Creating new user")
        # Create new user
        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        print("DEBUG: Committing transaction")
        conn.commit()
        
        print("DEBUG: Registration successful (without session)")
        return jsonify({
            'message': 'Registration successful',
            'user': {'id': cursor.lastrowid, 'username': username, 'email': email}
        }), 201
        
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        print("DEBUG: Closing database connection")
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    conn = get_db()
    try:
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            return jsonify({
                'message': 'Login successful',
                'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    conn = get_db()
    try:
        user = conn.execute(
            'SELECT id, username, email FROM users WHERE id = ?',
            (session['user_id'],)
        ).fetchone()
        
        if user:
            return jsonify({
                'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Timer routes
@app.route('/api/timer/sessions', methods=['GET'])
@login_required
def get_timer_sessions():
    conn = get_db()
    try:
        sessions = conn.execute(
            '''SELECT * FROM timer_sessions 
               WHERE user_id = ? 
               ORDER BY started_at DESC 
               LIMIT 50''',
            (session['user_id'],)
        ).fetchall()
        
        return jsonify({
            'sessions': [dict(session) for session in sessions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/timer/sessions', methods=['POST'])
@login_required
def create_timer_session():
    data = request.json
    session_type = data.get('session_type', 'work')
    duration = data.get('duration', 25)
    
    conn = get_db()
    try:
        cursor = conn.execute(
            '''INSERT INTO timer_sessions 
               (user_id, session_type, duration, started_at) 
               VALUES (?, ?, ?, ?)''',
            (session['user_id'], session_type, duration, datetime.now())
        )
        conn.commit()
        
        return jsonify({
            'message': 'Timer session created',
            'session_id': cursor.lastrowid
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/timer/sessions/<int:session_id>/complete', methods=['PUT'])
@login_required
def complete_timer_session(session_id):
    conn = get_db()
    try:
        conn.execute(
            '''UPDATE timer_sessions 
               SET completed = TRUE, completed_at = ? 
               WHERE id = ? AND user_id = ?''',
            (datetime.now(), session_id, session['user_id'])
        )
        conn.commit()
        
        return jsonify({'message': 'Session completed'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Timetable routes
@app.route('/api/timetables', methods=['GET'])
@login_required
def get_timetables():
    conn = get_db()
    try:
        timetables = conn.execute(
            '''SELECT t.*, COUNT(te.id) as entry_count
               FROM timetables t 
               LEFT JOIN timetable_entries te ON t.id = te.timetable_id
               WHERE t.user_id = ? 
               GROUP BY t.id
               ORDER BY t.date DESC''',
            (session['user_id'],)
        ).fetchall()
        
        return jsonify({
            'timetables': [dict(timetable) for timetable in timetables]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/timetables', methods=['POST'])
@login_required
def create_timetable():
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    date = data.get('date')
    entries = data.get('entries', [])
    
    if not title or not date:
        return jsonify({'error': 'Title and date are required'}), 400
    
    conn = get_db()
    try:
        # Create timetable
        cursor = conn.execute(
            '''INSERT INTO timetables (user_id, title, description, date) 
               VALUES (?, ?, ?, ?)''',
            (session['user_id'], title, description, date)
        )
        timetable_id = cursor.lastrowid
        
        # Create entries
        for entry in entries:
            conn.execute(
                '''INSERT INTO timetable_entries 
                   (timetable_id, start_time, end_time, subject, is_break) 
                   VALUES (?, ?, ?, ?, ?)''',
                (timetable_id, entry['start_time'], entry['end_time'], 
                 entry['subject'], entry.get('is_break', False))
            )
        
        conn.commit()
        
        return jsonify({
            'message': 'Timetable created successfully',
            'timetable_id': timetable_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/timetables/<int:timetable_id>', methods=['GET'])
@login_required
def get_timetable_details(timetable_id):
    conn = get_db()
    try:
        # Get timetable
        timetable = conn.execute(
            'SELECT * FROM timetables WHERE id = ? AND user_id = ?',
            (timetable_id, session['user_id'])
        ).fetchone()
        
        if not timetable:
            return jsonify({'error': 'Timetable not found'}), 404
        
        # Get entries
        entries = conn.execute(
            '''SELECT * FROM timetable_entries 
               WHERE timetable_id = ? 
               ORDER BY start_time''',
            (timetable_id,)
        ).fetchall()
        
        return jsonify({
            'timetable': dict(timetable),
            'entries': [dict(entry) for entry in entries]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Statistics route
@app.route('/api/stats', methods=['GET'])
@login_required
def get_user_stats():
    conn = get_db()
    try:
        # Total completed sessions
        total_sessions = conn.execute(
            'SELECT COUNT(*) as count FROM timer_sessions WHERE user_id = ? AND completed = TRUE',
            (session['user_id'],)
        ).fetchone()['count']
        
        # Total study time (in minutes)
        total_time = conn.execute(
            '''SELECT SUM(duration) as total FROM timer_sessions 
               WHERE user_id = ? AND completed = TRUE AND session_type = 'work' ''',
            (session['user_id'],)
        ).fetchone()['total'] or 0
        
        # Sessions this week
        week_ago = datetime.now() - timedelta(days=7)
        weekly_sessions = conn.execute(
            '''SELECT COUNT(*) as count FROM timer_sessions 
               WHERE user_id = ? AND completed = TRUE AND started_at > ?''',
            (session['user_id'], week_ago)
        ).fetchone()['count']
        
        return jsonify({
            'total_sessions': total_sessions,
            'total_study_time': total_time,
            'weekly_sessions': weekly_sessions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)