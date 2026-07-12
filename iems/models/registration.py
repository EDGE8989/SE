from datetime import datetime
from extensions import db

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    year = db.Column(db.String(20))  # 1st, 2nd, 3rd, 4th
    item_type = db.Column(db.String(50), nullable=False)  # event, workshop, scholarship, opportunity
    item_id = db.Column(db.Integer, nullable=False)
    item_title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)  # Optional cover letter / message
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Registration {self.name} for {self.item_type}:{self.item_id}>'
