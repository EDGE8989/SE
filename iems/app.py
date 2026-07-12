import os
from flask import Flask
from config import config
from extensions import db, login_manager, csrf

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'clubs'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'attachments'), exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    from routes.public import public_bp
    from routes.auth import auth_bp
    from routes.admin_dashboard import admin_bp
    from routes.admin_events import events_bp
    from routes.admin_notices import notices_bp
    from routes.admin_scholarships import scholarships_bp
    from routes.admin_workshops import workshops_bp
    from routes.admin_opportunities import opportunities_bp
    from routes.admin_calendar import calendar_bp
    from routes.admin_clubs import clubs_bp
    from routes.admin_users import users_bp
    from routes.admin_approvals import approvals_bp
    from routes.registration import registration_bp
    from routes.admin_registrations import registrations_bp
    from routes.access_request import access_request_bp
    from routes.admin_access_requests import admin_access_requests_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(notices_bp)
    app.register_blueprint(scholarships_bp)
    app.register_blueprint(workshops_bp)
    app.register_blueprint(opportunities_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(approvals_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(access_request_bp)
    app.register_blueprint(admin_access_requests_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        _seed_super_admin(app)
    
    @app.before_request
    def restrict_admin_access():
        from flask import request, redirect, url_for, flash
        from flask_login import current_user, logout_user
        if request.path.startswith('/admin'):
            if current_user.is_authenticated and current_user.role not in ('super_admin', 'college_admin', 'club_president'):
                logout_user()
                flash('Access denied. You do not have permission to access the admin panel.', 'danger')
                return redirect(url_for('auth.login'))
                
    return app

def _seed_super_admin(app):
    """Create default super admin if no users exist."""
    from models.user import User
    from extensions import db
    from werkzeug.security import generate_password_hash
    
    if User.query.count() == 0:
        super_admin = User(
            name='Super Admin',
            email='admin@iems.edu',
            password_hash=generate_password_hash('Admin@123'),
            role='super_admin',
            status='active'
        )
        db.session.add(super_admin)
        db.session.commit()
        print('[IEMS] Default Super Admin created: admin@iems.edu / Admin@123')

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
