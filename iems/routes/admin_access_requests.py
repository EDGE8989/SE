from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models.access_request import AccessRequest
from models.user import User
from models.club import Club
from utils.decorators import super_admin_required
from utils.helpers import log_activity
from werkzeug.security import generate_password_hash
import secrets
import string

admin_access_requests_bp = Blueprint('admin_access_requests', __name__, url_prefix='/admin/access-requests')

def _generate_temp_password(length=12):
    alphabet = string.ascii_letters + string.digits + '!@#$'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@admin_access_requests_bp.route('/')
@login_required
@super_admin_required
def index():
    status_filter = request.args.get('status', 'pending')
    query = AccessRequest.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    requests_list = query.order_by(AccessRequest.created_at.desc()).all()

    counts = {
        'pending': AccessRequest.query.filter_by(status='pending').count(),
        'approved': AccessRequest.query.filter_by(status='approved').count(),
        'rejected': AccessRequest.query.filter_by(status='rejected').count(),
    }

    return render_template('admin/access_requests.html',
        requests=requests_list,
        counts=counts,
        status_filter=status_filter
    )

@admin_access_requests_bp.route('/<int:id>/approve', methods=['POST'])
@login_required
@super_admin_required
def approve(id):
    access_req = AccessRequest.query.get_or_404(id)

    if access_req.status != 'pending':
        flash('This request has already been reviewed.', 'warning')
        return redirect(url_for('admin_access_requests.index'))

    # Check if user already exists
    if User.query.filter_by(email=access_req.email).first():
        flash('A user with this email already exists.', 'danger')
        access_req.status = 'rejected'
        access_req.review_note = 'Auto-rejected: Email already registered.'
        access_req.reviewed_by = current_user.id
        access_req.reviewed_at = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('admin_access_requests.index'))

    # Generate temporary password
    temp_password = _generate_temp_password()
    review_note = request.form.get('review_note', '').strip()

    # Determine club_id
    club_id = access_req.club_id

    new_user = User(
        name=access_req.name,
        email=access_req.email,
        password_hash=generate_password_hash(temp_password),
        role=access_req.requested_role,
        club_id=club_id,
        status='active'
    )
    db.session.add(new_user)

    access_req.status = 'approved'
    access_req.reviewed_by = current_user.id
    access_req.reviewed_at = datetime.utcnow()
    if review_note:
        access_req.review_note = f"{review_note} | Temp password: {temp_password}"
    else:
        access_req.review_note = f"Approved. Temp password: {temp_password}"

    db.session.commit()

    log_activity(current_user.id, 'APPROVE_ACCESS_REQUEST', 'Access Requests',
                 f'Approved request from {access_req.name} ({access_req.email}) as {access_req.role_display}')

    flash(f'Access request approved! Account created for {access_req.name}. '
          f'Temporary password: {temp_password}', 'success')
    return redirect(url_for('admin_access_requests.index'))

@admin_access_requests_bp.route('/<int:id>/reject', methods=['POST'])
@login_required
@super_admin_required
def reject(id):
    access_req = AccessRequest.query.get_or_404(id)

    if access_req.status != 'pending':
        flash('This request has already been reviewed.', 'warning')
        return redirect(url_for('admin_access_requests.index'))

    review_note = request.form.get('review_note', '').strip()
    access_req.status = 'rejected'
    access_req.reviewed_by = current_user.id
    access_req.reviewed_at = datetime.utcnow()
    access_req.review_note = review_note or 'Request rejected by admin.'
    db.session.commit()

    log_activity(current_user.id, 'REJECT_ACCESS_REQUEST', 'Access Requests',
                 f'Rejected request from {access_req.name} ({access_req.email})')

    flash(f'Access request from {access_req.name} has been rejected.', 'info')
    return redirect(url_for('admin_access_requests.index'))
