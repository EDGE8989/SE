from datetime import datetime
from extensions import db

class Notice(db.Model):
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='general')  # general, academic, club, recruitment
    attachment = db.Column(db.String(256))  # File path
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    approved_by_user = db.relationship('User', foreign_keys=[approved_by])
    
    @property
    def attachment_url(self):
        if self.attachment:
            return f'/static/uploads/attachments/{self.attachment}'
        return None
    
    @property
    def category_display(self):
        return {
            'general': 'General',
            'academic': 'Academic',
            'club': 'Club',
            'recruitment': 'Recruitment'
        }.get(self.category, self.category.title())
    
    def __repr__(self):
        return f'<Notice {self.title}>'
