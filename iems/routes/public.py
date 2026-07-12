from flask import Blueprint, render_template, request, abort
from datetime import datetime, date
from models.event import Event
from models.notice import Notice
from models.scholarship import Scholarship
from models.workshop import Workshop
from models.opportunity import Opportunity
from models.club import Club
from models.calendar_event import CalendarEvent
from extensions import db

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    # Upcoming approved events (next 30 days)
    upcoming_events = Event.query.filter(
        Event.status == 'approved',
        Event.date >= date.today()
    ).order_by(Event.date.asc()).limit(6).all()
    
    # Latest approved notices
    latest_notices = Notice.query.filter_by(status='approved').order_by(
        Notice.created_at.desc()).limit(5).all()
    
    # Featured clubs
    featured_clubs = Club.query.filter_by(is_active=True).limit(6).all()
    
    # Active scholarships
    scholarships = Scholarship.query.filter(
        db.or_(Scholarship.deadline >= date.today(), Scholarship.deadline.is_(None))
    ).order_by(Scholarship.deadline.asc()).limit(3).all()
    
    # Upcoming workshops
    upcoming_workshops = Workshop.query.filter(
        Workshop.status == 'approved',
        Workshop.date >= date.today()
    ).order_by(Workshop.date.asc()).limit(3).all()
    
    # Recent opportunities
    opportunities = Opportunity.query.filter(
        db.or_(Opportunity.deadline >= date.today(), Opportunity.deadline.is_(None))
    ).order_by(Opportunity.created_at.desc()).limit(4).all()
    
    # Calendar events this month
    today = date.today()
    calendar_events = CalendarEvent.query.filter(
        db.extract('month', CalendarEvent.event_date) == today.month,
        db.extract('year', CalendarEvent.event_date) == today.year
    ).order_by(CalendarEvent.event_date.asc()).all()
    
    # Stats
    stats = {
        'clubs': Club.query.filter_by(is_active=True).count(),
        'events': Event.query.filter_by(status='approved').count(),
        'students': 2500,  # Static count
        'scholarships': Scholarship.query.count()
    }
    
    return render_template('public/home.html',
        upcoming_events=upcoming_events,
        latest_notices=latest_notices,
        featured_clubs=featured_clubs,
        scholarships=scholarships,
        upcoming_workshops=upcoming_workshops,
        opportunities=opportunities,
        calendar_events=calendar_events,
        stats=stats,
        today=today
    )

@public_bp.route('/clubs')
def clubs():
    category = request.args.get('category', '')
    query = Club.query.filter_by(is_active=True)
    if category:
        query = query.filter_by(category=category)
    clubs = query.order_by(Club.name.asc()).all()
    categories = db.session.query(Club.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    return render_template('public/clubs.html', clubs=clubs, categories=categories, selected_category=category)

@public_bp.route('/clubs/<int:club_id>')
def club_detail(club_id):
    club = Club.query.get_or_404(club_id)
    events = Event.query.filter_by(club_id=club_id, status='approved').order_by(Event.date.desc()).limit(6).all()
    notices = Notice.query.filter_by(club_id=club_id, status='approved').order_by(Notice.created_at.desc()).limit(5).all()
    return render_template('public/club_detail.html', club=club, events=events, notices=notices)

@public_bp.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '')
    club_filter = request.args.get('club', 0, type=int)
    
    query = Event.query.filter_by(status='approved')
    if search:
        query = query.filter(Event.title.ilike(f'%{search}%'))
    if club_filter:
        query = query.filter_by(club_id=club_filter)
    
    pagination = query.order_by(Event.date.asc()).paginate(page=page, per_page=9, error_out=False)
    clubs = Club.query.filter_by(is_active=True).all()
    return render_template('public/events.html', pagination=pagination, clubs=clubs, search=search, club_filter=club_filter)

@public_bp.route('/events/<int:event_id>')
def event_detail(event_id):
    event = Event.query.filter_by(id=event_id, status='approved').first_or_404()
    related = Event.query.filter(
        Event.status == 'approved',
        Event.id != event_id,
        Event.club_id == event.club_id
    ).limit(3).all()
    return render_template('public/event_detail.html', event=event, related=related)

@public_bp.route('/notices')
def notices():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    query = Notice.query.filter_by(status='approved')
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.order_by(Notice.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('public/notices.html', pagination=pagination, category=category)

@public_bp.route('/scholarships')
def scholarships():
    active_scholarships = Scholarship.query.filter(
        db.or_(Scholarship.deadline >= date.today(), Scholarship.deadline.is_(None))
    ).order_by(Scholarship.deadline.asc()).all()
    past_scholarships = Scholarship.query.filter(
        Scholarship.deadline < date.today()
    ).order_by(Scholarship.deadline.desc()).limit(5).all()
    return render_template('public/scholarships.html', active_scholarships=active_scholarships, past_scholarships=past_scholarships)

@public_bp.route('/opportunities')
def opportunities():
    opp_type = request.args.get('type', '')
    query = Opportunity.query
    if opp_type:
        query = query.filter_by(type=opp_type)
    opportunities = query.order_by(Opportunity.created_at.desc()).all()
    return render_template('public/opportunities.html', opportunities=opportunities, opp_type=opp_type)

@public_bp.route('/workshops')
def workshops():
    page = request.args.get('page', 1, type=int)
    upcoming = Workshop.query.filter(
        Workshop.status == 'approved',
        Workshop.date >= date.today()
    ).order_by(Workshop.date.asc()).all()
    past = Workshop.query.filter(
        Workshop.status == 'approved',
        Workshop.date < date.today()
    ).order_by(Workshop.date.desc()).limit(6).all()
    return render_template('public/workshops.html', upcoming=upcoming, past=past)

@public_bp.route('/calendar')
def calendar():
    month = request.args.get('month', date.today().month, type=int)
    year = request.args.get('year', date.today().year, type=int)
    
    events = CalendarEvent.query.filter(
        db.extract('month', CalendarEvent.event_date) == month,
        db.extract('year', CalendarEvent.event_date) == year
    ).order_by(CalendarEvent.event_date.asc()).all()
    
    return render_template('public/calendar.html', events=events, month=month, year=year, today=date.today())

@public_bp.route('/updates')
def updates():
    recent_events = Event.query.filter_by(status='approved').order_by(Event.created_at.desc()).limit(5).all()
    recent_notices = Notice.query.filter_by(status='approved').order_by(Notice.created_at.desc()).limit(5).all()
    recent_scholarships = Scholarship.query.order_by(Scholarship.created_at.desc()).limit(5).all()
    recent_workshops = Workshop.query.filter_by(status='approved').order_by(Workshop.created_at.desc()).limit(5).all()
    recent_opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).limit(5).all()
    return render_template('public/updates.html',
        recent_events=recent_events,
        recent_notices=recent_notices,
        recent_scholarships=recent_scholarships,
        recent_workshops=recent_workshops,
        recent_opportunities=recent_opportunities
    )
