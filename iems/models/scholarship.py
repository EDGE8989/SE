from datetime import datetime
from extensions import db

class Scholarship(db.Model):
    __tablename__ = 'scholarships'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    deadline = db.Column(db.Date)
    application_link = db.Column(db.String(500))
    amount = db.Column(db.String(100))  # e.g. 'Rs. 50,000 per year'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_active(self):
        if self.deadline:
            return self.deadline >= datetime.utcnow().date()
        return True
    
    def __repr__(self):
        return f'<Scholarship {self.title}>'
