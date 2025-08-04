"""
Database Models for PomodoroFlow Application
"""

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, db_path='pomodoro.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
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
            session_type TEXT NOT NULL,
            duration INTEGER NOT NULL,
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

class User:
    def __init__(self, db):
        self.db = db
    
    def create(self, username, email, password):
        conn = self.db.get_connection()
        try:
            password_hash = generate_password_hash(password)
            cursor = conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def authenticate(self, username, password):
        conn = self.db.get_connection()
        try:
            user = conn.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                return dict(user)
            return None
        finally:
            conn.close()
    
    def get_by_id(self, user_id):
        conn = self.db.get_connection()
        try:
            user = conn.execute(
                'SELECT id, username, email, created_at FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()
    
    def exists(self, username=None, email=None):
        conn = self.db.get_connection()
        try:
            if username and email:
                user = conn.execute(
                    'SELECT id FROM users WHERE username = ? OR email = ?',
                    (username, email)
                ).fetchone()
            elif username:
                user = conn.execute(
                    'SELECT id FROM users WHERE username = ?',
                    (username,)
                ).fetchone()
            elif email:
                user = conn.execute(
                    'SELECT id FROM users WHERE email = ?',
                    (email,)
                ).fetchone()
            else:
                return False
            
            return user is not None
        finally:
            conn.close()

class TimerSession:
    def __init__(self, db):
        self.db = db
    
    def create(self, user_id, session_type, duration):
        conn = self.db.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO timer_sessions 
                   (user_id, session_type, duration, started_at) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, session_type, duration, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def complete(self, session_id, user_id):
        conn = self.db.get_connection()
        try:
            conn.execute(
                '''UPDATE timer_sessions 
                   SET completed = TRUE, completed_at = ? 
                   WHERE id = ? AND user_id = ?''',
                (datetime.now(), session_id, user_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()
    
    def get_user_sessions(self, user_id, limit=50):
        conn = self.db.get_connection()
        try:
            sessions = conn.execute(
                '''SELECT * FROM timer_sessions 
                   WHERE user_id = ? 
                   ORDER BY started_at DESC 
                   LIMIT ?''',
                (user_id, limit)
            ).fetchall()
            return [dict(session) for session in sessions]
        finally:
            conn.close()
    
    def get_user_stats(self, user_id):
        conn = self.db.get_connection()
        try:
            # Total completed sessions
            total_sessions = conn.execute(
                'SELECT COUNT(*) as count FROM timer_sessions WHERE user_id = ? AND completed = TRUE',
                (user_id,)
            ).fetchone()['count']
            
            # Total study time
            total_time = conn.execute(
                '''SELECT SUM(duration) as total FROM timer_sessions 
                   WHERE user_id = ? AND completed = TRUE AND session_type = 'work' ''',
                (user_id,)
            ).fetchone()['total'] or 0
            
            # Sessions this week
            from datetime import timedelta
            week_ago = datetime.now() - timedelta(days=7)
            weekly_sessions = conn.execute(
                '''SELECT COUNT(*) as count FROM timer_sessions 
                   WHERE user_id = ? AND completed = TRUE AND started_at > ?''',
                (user_id, week_ago)
            ).fetchone()['count']
            
            return {
                'total_sessions': total_sessions,
                'total_study_time': total_time,
                'weekly_sessions': weekly_sessions
            }
        finally:
            conn.close()

class Timetable:
    def __init__(self, db):
        self.db = db
    
    def create(self, user_id, title, description, date):
        conn = self.db.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO timetables (user_id, title, description, date) 
                   VALUES (?, ?, ?, ?)''',
                (user_id, title, description, date)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def add_entry(self, timetable_id, start_time, end_time, subject, is_break=False):
        conn = self.db.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO timetable_entries 
                   (timetable_id, start_time, end_time, subject, is_break) 
                   VALUES (?, ?, ?, ?, ?)''',
                (timetable_id, start_time, end_time, subject, is_break)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def get_user_timetables(self, user_id):
        conn = self.db.get_connection()
        try:
            timetables = conn.execute(
                '''SELECT t.*, COUNT(te.id) as entry_count
                   FROM timetables t 
                   LEFT JOIN timetable_entries te ON t.id = te.timetable_id
                   WHERE t.user_id = ? 
                   GROUP BY t.id
                   ORDER BY t.date DESC''',
                (user_id,)
            ).fetchall()
            return [dict(timetable) for timetable in timetables]
        finally:
            conn.close()
    
    def get_timetable_with_entries(self, timetable_id, user_id):
        conn = self.db.get_connection()
        try:
            # Get timetable
            timetable = conn.execute(
                'SELECT * FROM timetables WHERE id = ? AND user_id = ?',
                (timetable_id, user_id)
            ).fetchone()
            
            if not timetable:
                return None
            
            # Get entries
            entries = conn.execute(
                '''SELECT * FROM timetable_entries 
                   WHERE timetable_id = ? 
                   ORDER BY start_time''',
                (timetable_id,)
            ).fetchall()
            
            return {
                'timetable': dict(timetable),
                'entries': [dict(entry) for entry in entries]
            }
        finally:
            conn.close()
    
    def delete(self, timetable_id, user_id):
        conn = self.db.get_connection()
        try:
            # Delete entries first
            conn.execute(
                'DELETE FROM timetable_entries WHERE timetable_id = ?',
                (timetable_id,)
            )
            
            # Delete timetable
            conn.execute(
                'DELETE FROM timetables WHERE id = ? AND user_id = ?',
                (timetable_id, user_id)
            )
            
            conn.commit()
            return True
        finally:
            conn.close()