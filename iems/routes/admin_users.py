from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.club import Club
from utils.decorators import role_required
from utils.helpers import log_activity
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/admin/users')

@users_bp.route('/')
@login_required
@role_required('super_admin')
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    clubs = Club.query.filter_by(is_active=True).all()
    return render_template('admin/users.html', users=users, clubs=clubs)

@users_bp.route('/add', methods=['POST'])
@login_required
@role_required('super_admin')
def add():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    club_id = request.form.get('club_id')
    
    existing = User.query.filter_by(email=email).first()
    if existing:
        flash('A user with that email already exists.', 'danger')
        return redirect(url_for('users.index'))
        
    club_id = int(club_id) if club_id else None
        
    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        club_id=club_id
    )
    
    db.session.add(user)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_USER', 'Users', f'Created {role}: {name}')
    flash('User account created successfully!', 'success')
    return redirect(url_for('users.index'))

@users_bp.route('/<int:id>/toggle_status', methods=['POST'])
@login_required
@role_required('super_admin')
def toggle_status(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('users.index'))
        
    user.status = 'inactive' if user.status == 'active' else 'active'
    db.session.commit()
    
    log_activity(current_user.id, 'TOGGLE_USER', 'Users', f'Set {user.name} to {user.status}')
    flash(f'User account is now {user.status}.', 'success')
    return redirect(url_for('users.index'))
