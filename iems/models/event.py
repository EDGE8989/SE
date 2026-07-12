from datetime import datetime
from extensions import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    venue = db.Column(db.String(200))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    image = db.Column(db.String(256))
    registration_link = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def image_url(self):
        if self.image:
            return f'/static/uploads/events/{self.image}'
        return '/static/images/event_default.jpg'
    
    @property
    def is_upcoming(self):
        if self.date:
            return self.date >= datetime.utcnow().date()
        return False
    
    @property
    def status_badge(self):
        return {
            'pending': 'badge-warning',
            'approved': 'badge-success',
            'rejected': 'badge-danger'
        }.get(self.status, 'badge-secondary')
    
    def __repr__(self):
        return f'<Event {self.title}>'
