import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from extensions import db

def allowed_file(filename, file_type='image'):
    """Check if file extension is allowed."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'image':
        return ext in current_app.config['ALLOWED_IMAGE_EXTENSIONS']
    elif file_type == 'document':
        return ext in current_app.config['ALLOWED_DOC_EXTENSIONS']
    return False

def save_upload(file, subfolder='', file_type='image'):
    """Save uploaded file securely and return the filename."""
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename, file_type):
        return None
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    safe_name = secure_filename(unique_name)
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_path, exist_ok=True)
    
    file.save(os.path.join(upload_path, safe_name))
    return safe_name

def log_activity(user_id, action, module, details=None):
    """Log an admin action to the activity_logs table."""
    from models.activity_log import ActivityLog
    from flask import request
    
    log = ActivityLog(
        user_id=user_id,
        action=action,
        module=module,
        details=details,
        ip_address=request.remote_addr if request else None,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()

def get_pagination_args(request, default_per_page=10):
    """Extract pagination parameters from request."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default_per_page, type=int)
    return page, per_page

def time_ago(dt):
    """Return a human-readable time difference."""
    if not dt:
        return 'Unknown'
    now = datetime.utcnow()
    diff = now - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        return f'{int(seconds/60)} min ago'
    elif seconds < 86400:
        return f'{int(seconds/3600)} hr ago'
    elif seconds < 604800:
        return f'{int(seconds/86400)} days ago'
    else:
        return dt.strftime('%d %b %Y')
