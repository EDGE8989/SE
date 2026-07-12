from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.club import Club
from models.event import Event
from models.user import User
from models.notice import Notice
from models.activity_log import ActivityLog

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    stats = {}
    if current_user.is_super_admin or current_user.is_college_admin:
        stats = {
            'clubs': Club.query.count(),
            'events': Event.query.count(),
            'users': User.query.count(),
            'notices': Notice.query.count()
        }
    elif current_user.is_club_president and current_user.club_id:
        stats = {
            'events': Event.query.filter_by(club_id=current_user.club_id).count(),
            'notices': Notice.query.filter_by(club_id=current_user.club_id).count(),
        }
        
    recent_activity = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_activity=recent_activity)
