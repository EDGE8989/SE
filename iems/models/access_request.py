from datetime import datetime
from extensions import db

class AccessRequest(db.Model):
    __tablename__ = 'access_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    requested_role = db.Column(db.String(50), nullable=False)  # college_admin, club_president
    club_name = db.Column(db.String(100))     # if requesting club_president role
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    designation = db.Column(db.String(100))   # e.g. "Head of Department"
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    review_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    club = db.relationship('Club', foreign_keys=[club_id])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])

    @property
    def role_display(self):
        return {
            'college_admin': 'College Admin',
            'club_president': 'Club / Society President'
        }.get(self.requested_role, self.requested_role.title())

    def __repr__(self):
        return f'<AccessRequest {self.name} ({self.requested_role}) - {self.status}>'
