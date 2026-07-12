from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.club import Club
from utils.decorators import role_required
from utils.helpers import save_upload, log_activity

clubs_bp = Blueprint('clubs', __name__, url_prefix='/admin/clubs')

@clubs_bp.route('/')
@login_required
@role_required('super_admin', 'college_admin')
def index():
    clubs = Club.query.order_by(Club.name.asc()).all()
    return render_template('admin/clubs.html', clubs=clubs)

@clubs_bp.route('/add', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def add():
    name = request.form.get('name')
    category = request.form.get('category')
    president = request.form.get('president')
    faculty = request.form.get('faculty')
    email = request.form.get('email')
    description = request.form.get('description')
    
    logo_file = request.files.get('logo')
    logo_filename = None
    if logo_file:
        logo_filename = save_upload(logo_file, subfolder='clubs', file_type='image')
        
    club = Club(
        name=name,
        category=category,
        president=president,
        faculty=faculty,
        email=email,
        description=description,
        logo=logo_filename
    )
    
    db.session.add(club)
    db.session.commit()
    log_activity(current_user.id, 'CREATE_CLUB', 'Clubs', f'Created club: {name}')
    flash('Club added successfully!', 'success')
    
    return redirect(url_for('clubs.index'))

@clubs_bp.route('/<int:id>/toggle_status', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def toggle_status(id):
    club = Club.query.get_or_404(id)
    club.is_active = not club.is_active
    db.session.commit()
    status = "activated" if club.is_active else "deactivated"
    log_activity(current_user.id, 'TOGGLE_CLUB', 'Clubs', f'{status.title()} club: {club.name}')
    flash(f'Club {status} successfully!', 'success')
    return redirect(url_for('clubs.index'))

@clubs_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('super_admin')
def delete(id):
    club = Club.query.get_or_404(id)
    name = club.name
    db.session.delete(club)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_CLUB', 'Clubs', f'Deleted club: {name}')
    flash('Club deleted successfully!', 'success')
    return redirect(url_for('clubs.index'))
