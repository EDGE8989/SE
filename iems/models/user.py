from datetime import datetime
from flask_login import UserMixin
from extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='club_president')
    # Roles: super_admin, college_admin, club_president
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    club = db.relationship('Club', foreign_keys=[club_id], backref='president_user')
    created_events = db.relationship('Event', foreign_keys='Event.created_by', backref='creator', lazy='dynamic')
    approved_events = db.relationship('Event', foreign_keys='Event.approved_by', backref='approver', lazy='dynamic')
    created_notices = db.relationship('Notice', foreign_keys='Notice.created_by', backref='creator', lazy='dynamic')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_college_admin(self):
        return self.role == 'college_admin'

    @property
    def is_club_president(self):
        return self.role == 'club_president'

    @property
    def can_approve(self):
        return self.role in ('super_admin', 'college_admin')

    @property
    def role_display(self):
        return {
            'super_admin': 'Super Admin',
            'college_admin': 'College Admin',
            'club_president': 'Club President'
        }.get(self.role, self.role)

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
