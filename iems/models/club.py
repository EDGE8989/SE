from extensions import db

class Club(db.Model):
    __tablename__ = 'clubs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo = db.Column(db.String(256))  # File path
    faculty = db.Column(db.String(100))  # Faculty advisor
    president = db.Column(db.String(100))  # President name (display)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    category = db.Column(db.String(50), default='general')  # technical, cultural, sports, general
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    events = db.relationship('Event', backref='club', lazy='dynamic')
    notices = db.relationship('Notice', backref='club', lazy='dynamic')
    
    @property
    def logo_url(self):
        if self.logo:
            return f'/static/uploads/clubs/{self.logo}'
        return '/static/images/club_default.png'
    
    def __repr__(self):
        return f'<Club {self.name}>'
