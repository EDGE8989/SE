from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.notice import Notice
from models.club import Club
from utils.helpers import save_upload, log_activity

notices_bp = Blueprint('notices', __name__, url_prefix='/admin/notices')

@notices_bp.route('/')
@login_required
def index():
    if current_user.role == 'club_president':
        notices = Notice.query.filter_by(club_id=current_user.club_id).order_by(Notice.created_at.desc()).all()
    else:
        notices = Notice.query.order_by(Notice.created_at.desc()).all()
        
    clubs = Club.query.filter_by(is_active=True).all()
    return render_template('admin/notices.html', notices=notices, clubs=clubs)

@notices_bp.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    club_id = request.form.get('club_id')
    
    if current_user.role == 'club_president':
        club_id = current_user.club_id
    elif club_id:
        club_id = int(club_id)
        
    attachment_file = request.files.get('attachment')
    attachment_filename = None
    if attachment_file:
        attachment_filename = save_upload(attachment_file, subfolder='attachments', file_type='document')
        if not attachment_filename: # Maybe they uploaded a PDF but we used document checking. wait, helpers.py allows 'document' -> pdf, doc. We'll use 'document'
            pass
            
    status = 'approved'
    
    notice = Notice(
        title=title,
        category=category,
        description=description,
        attachment=attachment_filename,
        club_id=club_id,
        created_by=current_user.id,
        status=status
    )
    
    notice.approved_by = current_user.id
        
    db.session.add(notice)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_NOTICE', 'Notices', f'Created notice: {title}')
    flash('Notice published successfully!', 'success')
    return redirect(url_for('notices.index'))

@notices_bp.route('/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    if not current_user.can_approve:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('notices.index'))
        
    notice = Notice.query.get_or_404(id)
    status = request.form.get('status')
    
    if status in ['approved', 'rejected', 'pending']:
        notice.status = status
        if status == 'approved':
            notice.approved_by = current_user.id
        db.session.commit()
        log_activity(current_user.id, 'UPDATE_NOTICE_STATUS', 'Notices', f'Updated notice {notice.title} to {status}')
        flash(f'Notice status updated to {status}.', 'success')
        
    return redirect(url_for('notices.index'))

@notices_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    notice = Notice.query.get_or_404(id)
    
    is_authorized = False
    if current_user.role in ('super_admin', 'college_admin'):
        is_authorized = True
    elif current_user.role == 'club_president' and notice.club_id == current_user.club_id:
        is_authorized = True
        
    if not is_authorized:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('notices.index'))
        
    title = notice.title
    db.session.delete(notice)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_NOTICE', 'Notices', f'Deleted notice: {title}')
    flash('Notice deleted successfully.', 'success')
    return redirect(url_for('notices.index'))
