from datetime import datetime
from extensions import db

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200), nullable=False)
    module = db.Column(db.String(50))  # events, notices, users, clubs, etc.
    details = db.Column(db.Text)  # JSON string for extra context
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action} by user {self.user_id}>'
