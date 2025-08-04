"""
Database Configuration and Connection Management
"""

import sqlite3
import os
from contextlib import contextmanager

class DatabaseConfig:
    def __init__(self, db_path='pomodoro.db'):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Ensure the database file exists and create it if it doesn't"""
        if not os.path.exists(self.db_path):
            self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize the database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Enable foreign key constraints
            cursor.execute('PRAGMA foreign_keys = ON')
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Timer sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timer_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_type TEXT NOT NULL CHECK(session_type IN ('work', 'break')),
                    duration INTEGER NOT NULL CHECK(duration > 0),
                    completed BOOLEAN DEFAULT FALSE,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Timetables table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timetables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Timetable entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timetable_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timetable_id INTEGER NOT NULL,
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    subject TEXT NOT NULL,
                    is_break BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (timetable_id) REFERENCES timetables (id) ON DELETE CASCADE
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timer_sessions_user_id ON timer_sessions(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timer_sessions_started_at ON timer_sessions(started_at)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timetables_user_id ON timetables(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timetables_date ON timetables(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timetable_entries_timetable_id ON timetable_entries(timetable_id)')
            
            conn.commit()
    
    def get_db_info(self):
        """Get database information for debugging"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Get row counts
            table_info = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_info[table] = count
            
            return {
                'database_path': self.db_path,
                'tables': tables,
                'row_counts': table_info
            }
    
    def reset_database(self):
        """Reset the database by dropping all tables and recreating them"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Drop all tables
            cursor.execute("DROP TABLE IF EXISTS timetable_entries")
            cursor.execute("DROP TABLE IF EXISTS timetables") 
            cursor.execute("DROP TABLE IF EXISTS timer_sessions")
            cursor.execute("DROP TABLE IF EXISTS users")
            
            conn.commit()
        
        # Reinitialize
        self.init_database()

# Global database instance
db_config = DatabaseConfig()