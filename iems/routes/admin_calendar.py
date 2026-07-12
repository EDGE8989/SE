from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.calendar_event import CalendarEvent
from utils.decorators import role_required
from utils.helpers import log_activity
from datetime import datetime

calendar_bp = Blueprint('calendar', __name__, url_prefix='/admin/calendar')

@calendar_bp.route('/')
@login_required
@role_required('super_admin', 'college_admin')
def index():
    events = CalendarEvent.query.order_by(CalendarEvent.event_date.asc()).all()
    return render_template('admin/calendar.html', events=events)

@calendar_bp.route('/add', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    event_date_str = request.form.get('event_date')
    end_date_str = request.form.get('end_date')
    
    event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date() if event_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    
    category_color = {
        'exam': '#dc3545',
        'holiday': '#28a745',
        'event': '#0d6efd',
        'academic': '#6610f2'
    }.get(category, '#6c757d')
    
    cal_event = CalendarEvent(
        title=title,
        description=description,
        event_date=event_date,
        end_date=end_date,
        category=category,
        category_color=category_color
    )
    
    db.session.add(cal_event)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_CALENDAR_EVENT', 'Calendar', f'Created: {title}')
    flash('Calendar event added successfully!', 'success')
    return redirect(url_for('calendar.index'))

@calendar_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def delete(id):
    cal_event = CalendarEvent.query.get_or_404(id)
    title = cal_event.title
    db.session.delete(cal_event)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_CALENDAR_EVENT', 'Calendar', f'Deleted: {title}')
    flash('Calendar event deleted successfully.', 'success')
    return redirect(url_for('calendar.index'))
