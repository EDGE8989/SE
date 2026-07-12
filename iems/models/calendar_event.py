from extensions import db

class CalendarEvent(db.Model):
    __tablename__ = 'calendar_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # For multi-day events
    category = db.Column(db.String(50), default='event')  # exam, holiday, semester, event
    description = db.Column(db.Text)
    
    @property
    def category_color(self):
        return {
            'exam': '#EF4444',
            'holiday': '#10B981',
            'semester': '#2563EB',
            'event': '#F59E0B'
        }.get(self.category, '#6B7280')
    
    def __repr__(self):
        return f'<CalendarEvent {self.title} on {self.event_date}>'
