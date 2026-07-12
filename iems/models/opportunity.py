from datetime import datetime
from extensions import db

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100))
    type = db.Column(db.String(50), default='internship')  # internship, job, fellowship, competition
    description = db.Column(db.Text)
    deadline = db.Column(db.Date)
    application_link = db.Column(db.String(500))
    stipend = db.Column(db.String(100))  # e.g. 'Rs. 15,000/month'
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def type_display(self):
        return {
            'internship': 'Internship',
            'job': 'Job',
            'fellowship': 'Fellowship',
            'competition': 'Competition'
        }.get(self.type, self.type.title())
    
    @property
    def is_active(self):
        if self.deadline:
            return self.deadline >= datetime.utcnow().date()
        return True
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'
