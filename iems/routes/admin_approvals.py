from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.event import Event
from models.notice import Notice
from models.workshop import Workshop
from utils.decorators import role_required

approvals_bp = Blueprint('approvals', __name__, url_prefix='/admin/approvals')

@approvals_bp.route('/')
@login_required
@role_required('super_admin', 'college_admin')
def index():
    pending_events = Event.query.filter_by(status='pending').order_by(Event.created_at.desc()).all()
    pending_notices = Notice.query.filter_by(status='pending').order_by(Notice.created_at.desc()).all()
    pending_workshops = Workshop.query.filter_by(status='pending').order_by(Workshop.created_at.desc()).all()
    
    return render_template('admin/approvals.html', 
        pending_events=pending_events,
        pending_notices=pending_notices,
        pending_workshops=pending_workshops
    )
