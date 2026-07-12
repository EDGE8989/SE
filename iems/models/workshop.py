from datetime import datetime
from extensions import db

class Workshop(db.Model):
    __tablename__ = 'workshops'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    speaker = db.Column(db.String(100))
    venue = db.Column(db.String(200))
    registration_link = db.Column(db.String(500))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', foreign_keys=[created_by])
    approver = db.relationship('User', foreign_keys=[approved_by])
    
    @property
    def is_upcoming(self):
        if self.date:
            return self.date >= datetime.utcnow().date()
        return False
    
    def __repr__(self):
        return f'<Workshop {self.title}>'
