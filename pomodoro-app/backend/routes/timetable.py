"""
Timetable management routes for PomodoroFlow API
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime, time
from .auth import login_required
from ..models import Database, Timetable

timetable_bp = Blueprint('timetable', __name__)
db = Database()
timetable_model = Timetable(db)

@timetable_bp.route('', methods=['GET'])
@login_required
def get_timetables():
    """Get user's timetables"""
    try:
        timetables = timetable_model.get_user_timetables(session['user_id'])
        return jsonify({
            'success': True,
            'timetables': timetables
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching timetables: {str(e)}'
        }), 500

@timetable_bp.route('', methods=['POST'])
@login_required
def create_timetable():
    """Create a new timetable"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'schedule']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: name, schedule'
            }), 400
        
        # Validate schedule format
        if not isinstance(data['schedule'], list):
            return jsonify({
                'success': False,
                'message': 'Schedule must be an array of time blocks'
            }), 400
        
        # Validate each time block in schedule
        for block in data['schedule']:
            if not all(key in block for key in ['day', 'start_time', 'end_time', 'subject']):
                return jsonify({
                    'success': False,
                    'message': 'Each schedule block must have day, start_time, end_time, and subject'
                }), 400
            
            # Validate time format (HH:MM)
            try:
                start_time = datetime.strptime(block['start_time'], '%H:%M').time()
                end_time = datetime.strptime(block['end_time'], '%H:%M').time()
                
                if start_time >= end_time:
                    return jsonify({
                        'success': False,
                        'message': 'Start time must be before end time'
                    }), 400
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid time format. Use HH:MM format'
                }), 400
            
            # Validate day
            valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if block['day'].lower() not in valid_days:
                return jsonify({
                    'success': False,
                    'message': 'Invalid day. Use full day names (monday, tuesday, etc.)'
                }), 400
        
        timetable_id = timetable_model.create_timetable(
            user_id=session['user_id'],
            name=data['name'],
            description=data.get('description', ''),
            schedule=data['schedule']
        )
        
        return jsonify({
            'success': True,
            'message': 'Timetable created successfully',
            'timetable_id': timetable_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating timetable: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>', methods=['GET'])
@login_required
def get_timetable(timetable_id):
    """Get a specific timetable"""
    try:
        timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        
        if not timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        return jsonify({
            'success': True,
            'timetable': timetable
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching timetable: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>', methods=['PUT'])
@login_required
def update_timetable(timetable_id):
    """Update a timetable"""
    try:
        data = request.get_json()
        
        # Check if timetable exists and belongs to user
        existing_timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        if not existing_timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        # Validate schedule if provided
        if 'schedule' in data:
            if not isinstance(data['schedule'], list):
                return jsonify({
                    'success': False,
                    'message': 'Schedule must be an array of time blocks'
                }), 400
            
            # Validate each time block
            for block in data['schedule']:
                if not all(key in block for key in ['day', 'start_time', 'end_time', 'subject']):
                    return jsonify({
                        'success': False,
                        'message': 'Each schedule block must have day, start_time, end_time, and subject'
                    }), 400
                
                try:
                    start_time = datetime.strptime(block['start_time'], '%H:%M').time()
                    end_time = datetime.strptime(block['end_time'], '%H:%M').time()
                    
                    if start_time >= end_time:
                        return jsonify({
                            'success': False,
                            'message': 'Start time must be before end time'
                        }), 400
                except ValueError:
                    return jsonify({
                        'success': False,
                        'message': 'Invalid time format. Use HH:MM format'
                    }), 400
        
        success = timetable_model.update_timetable(
            timetable_id=timetable_id,
            user_id=session['user_id'],
            name=data.get('name'),
            description=data.get('description'),
            schedule=data.get('schedule')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Timetable updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update timetable'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating timetable: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>', methods=['DELETE'])
@login_required
def delete_timetable(timetable_id):
    """Delete a timetable"""
    try:
        # Check if timetable exists and belongs to user
        existing_timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        if not existing_timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        success = timetable_model.delete_timetable(timetable_id, session['user_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Timetable deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete timetable'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting timetable: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>/current', methods=['GET'])
@login_required
def get_current_session(timetable_id):
    """Get current session based on timetable and current time"""
    try:
        timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        
        if not timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        current_time = datetime.now()
        current_day = current_time.strftime('%A').lower()
        current_time_str = current_time.strftime('%H:%M')
        
        current_session = None
        next_session = None
        
        # Find current and next sessions
        for block in timetable['schedule']:
            if block['day'].lower() == current_day:
                start_time = datetime.strptime(block['start_time'], '%H:%M').time()
                end_time = datetime.strptime(block['end_time'], '%H:%M').time()
                current_time_obj = datetime.strptime(current_time_str, '%H:%M').time()
                
                if start_time <= current_time_obj <= end_time:
                    current_session = block
                elif start_time > current_time_obj:
                    if not next_session or start_time < datetime.strptime(next_session['start_time'], '%H:%M').time():
                        next_session = block
        
        return jsonify({
            'success': True,
            'current_session': current_session,
            'next_session': next_session,
            'current_time': current_time_str,
            'current_day': current_day
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting current session: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>/day/<string:day>', methods=['GET'])
@login_required
def get_day_schedule(timetable_id, day):
    """Get schedule for a specific day"""
    try:
        timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        
        if not timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day.lower() not in valid_days:
            return jsonify({
                'success': False,
                'message': 'Invalid day. Use full day names (monday, tuesday, etc.)'
            }), 400
        
        day_schedule = [block for block in timetable['schedule'] if block['day'].lower() == day.lower()]
        
        # Sort by start time
        day_schedule.sort(key=lambda x: datetime.strptime(x['start_time'], '%H:%M').time())
        
        return jsonify({
            'success': True,
            'day': day.lower(),
            'schedule': day_schedule
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting day schedule: {str(e)}'
        }), 500

@timetable_bp.route('/<int:timetable_id>/active', methods=['POST'])
@login_required
def set_active_timetable(timetable_id):
    """Set a timetable as the active one for the user"""
    try:
        # Check if timetable exists and belongs to user
        timetable = timetable_model.get_timetable(timetable_id, session['user_id'])
        if not timetable:
            return jsonify({
                'success': False,
                'message': 'Timetable not found'
            }), 404
        
        success = timetable_model.set_active_timetable(session['user_id'], timetable_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Timetable set as active'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to set active timetable'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error setting active timetable: {str(e)}'
        }), 500

@timetable_bp.route('/active', methods=['GET'])
@login_required
def get_active_timetable():
    """Get the user's active timetable"""
    try:
        active_timetable = timetable_model.get_active_timetable(session['user_id'])
        
        return jsonify({
            'success': True,
            'active_timetable': active_timetable
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting active timetable: {str(e)}'
        }), 500