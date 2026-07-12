from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.event import Event
from models.club import Club
from utils.helpers import save_upload, log_activity
from datetime import datetime

events_bp = Blueprint('events', __name__, url_prefix='/admin/events')

@events_bp.route('/')
@login_required
def index():
    if current_user.role == 'club_president':
        events = Event.query.filter_by(club_id=current_user.club_id).order_by(Event.created_at.desc()).all()
    else:
        events = Event.query.order_by(Event.created_at.desc()).all()
    
    clubs = Club.query.filter_by(is_active=True).all()
    return render_template('admin/events.html', events=events, clubs=clubs)

@events_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    venue = request.form.get('venue')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    registration_link = request.form.get('registration_link')
    club_id = request.form.get('club_id')
    
    if current_user.role == 'club_president':
        club_id = current_user.club_id
    elif club_id:
        club_id = int(club_id)
        
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    time_obj = datetime.strptime(time_str, '%H:%M').time() if time_str else None
    
    image_file = request.files.get('image')
    image_filename = None
    if image_file:
        image_filename = save_upload(image_file, subfolder='events', file_type='image')
        
    status = 'approved'
    
    event = Event(
        title=title,
        description=description,
        venue=venue,
        date=date_obj,
        time=time_obj,
        registration_link=registration_link,
        club_id=club_id,
        created_by=current_user.id,
        status=status,
        image=image_filename
    )
    
    event.approved_by = current_user.id
        
    db.session.add(event)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_EVENT', 'Events', f'Created event: {title}')
    flash('Event published successfully!', 'success')
    return redirect(url_for('events.index'))

@events_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.can_approve:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('events.index'))
        
    event = Event.query.get_or_404(id)
    status = request.form.get('status')
    
    if status in ['approved', 'rejected', 'pending']:
        event.status = status
        if status == 'approved':
            event.approved_by = current_user.id
        db.session.commit()
        log_activity(current_user.id, 'UPDATE_EVENT_STATUS', 'Events', f'Updated event {event.title} to {status}')
        flash(f'Event status updated to {status}.', 'success')
        
    return redirect(url_for('events.index'))

@events_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    event = Event.query.get_or_404(id)
    
    is_authorized = False
    if current_user.role in ('super_admin', 'college_admin'):
        is_authorized = True
    elif current_user.role == 'club_president' and event.club_id == current_user.club_id:
        is_authorized = True
        
    if not is_authorized:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('events.index'))
        
    title = event.title
    db.session.delete(event)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_EVENT', 'Events', f'Deleted event: {title}')
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('events.index'))
