"""
Routes package for PomodoroFlow API
"""

from .auth import auth_bp
from .timer import timer_bp  
from .timetable import timetable_bp

def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(timer_bp, url_prefix='/api/timer')
    app.register_blueprint(timetable_bp, url_prefix='/api/timetables')