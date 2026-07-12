from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """Decorator to restrict access to specific roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('admin.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for college_admin or super_admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role not in ('super_admin', 'college_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    """Decorator for super_admin only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role != 'super_admin':
            flash('Super Admin access required.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def club_owner_required(f):
    """Decorator ensuring club presidents can only manage their own club."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.role == 'club_president' and not current_user.club_id:
            flash('You are not assigned to any club.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function
