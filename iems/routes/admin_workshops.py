from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.workshop import Workshop
from utils.helpers import log_activity
from datetime import datetime

workshops_bp = Blueprint('workshops', __name__, url_prefix='/admin/workshops')

@workshops_bp.route('/')
@login_required
def index():
    if current_user.role == 'club_president':
        workshops = Workshop.query.filter_by(created_by=current_user.id).order_by(Workshop.created_at.desc()).all()
    else:
        workshops = Workshop.query.order_by(Workshop.created_at.desc()).all()
    return render_template('admin/workshops.html', workshops=workshops)

@workshops_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    speaker = request.form.get('speaker')
    venue = request.form.get('venue')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    registration_link = request.form.get('registration_link')
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    time_obj = datetime.strptime(time_str, '%H:%M').time() if time_str else None
    
    status = 'approved'
    
    workshop = Workshop(
        title=title,
        description=description,
        speaker=speaker,
        venue=venue,
        date=date_obj,
        time=time_obj,
        registration_link=registration_link,
        status=status,
        created_by=current_user.id
    )
    
    workshop.approved_by = current_user.id
        
    db.session.add(workshop)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_WORKSHOP', 'Workshops', f'Created workshop: {title}')
    flash('Workshop published successfully!', 'success')
    return redirect(url_for('workshops.index'))

@workshops_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.can_approve:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('workshops.index'))
        
    workshop = Workshop.query.get_or_404(id)
    status = request.form.get('status')
    
    if status in ['approved', 'rejected', 'pending']:
        workshop.status = status
        if status == 'approved':
            workshop.approved_by = current_user.id
        db.session.commit()
        log_activity(current_user.id, 'UPDATE_WORKSHOP_STATUS', 'Workshops', f'Updated workshop {workshop.title} to {status}')
        flash(f'Workshop status updated to {status}.', 'success')
        
    return redirect(url_for('workshops.index'))

@workshops_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    workshop = Workshop.query.get_or_404(id)
    
    is_authorized = False
    if current_user.role in ('super_admin', 'college_admin'):
        is_authorized = True
    elif current_user.role == 'club_president' and workshop.created_by == current_user.id:
        is_authorized = True
        
    if not is_authorized:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('workshops.index'))
        
    title = workshop.title
    db.session.delete(workshop)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_WORKSHOP', 'Workshops', f'Deleted workshop: {title}')
    flash('Workshop deleted successfully.', 'success')
    return redirect(url_for('workshops.index'))
