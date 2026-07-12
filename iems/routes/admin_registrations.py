from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from flask_login import login_required, current_user
from extensions import db
from models.registration import Registration
import csv
import io

registrations_bp = Blueprint('registrations', __name__, url_prefix='/admin/registrations')

def _filter_registrations_by_role(query):
    if current_user.role == 'club_president':
        from models.event import Event
        from models.workshop import Workshop
        club_event_ids = [e.id for e in Event.query.filter_by(club_id=current_user.club_id).all()]
        my_workshop_ids = [w.id for w in Workshop.query.filter_by(created_by=current_user.id).all()]
        
        filter_conds = []
        if club_event_ids:
            filter_conds.append(db.and_(Registration.item_type == 'event', Registration.item_id.in_(club_event_ids)))
        if my_workshop_ids:
            filter_conds.append(db.and_(Registration.item_type == 'workshop', Registration.item_id.in_(my_workshop_ids)))
            
        if filter_conds:
            query = query.filter(db.or_(*filter_conds))
        else:
            query = query.filter(db.false())
    return query

@registrations_bp.route('/')
@login_required
def index():
    if current_user.role not in ('super_admin', 'college_admin', 'club_president'):
        abort(403)
        
    item_type = request.args.get('type', '')
    query = Registration.query
    if item_type:
        query = query.filter_by(item_type=item_type)
        
    query = _filter_registrations_by_role(query)
    registrations = query.order_by(Registration.created_at.desc()).all()
    
    # Get counts by type
    all_query = _filter_registrations_by_role(Registration.query)
    event_query = _filter_registrations_by_role(Registration.query.filter_by(item_type='event'))
    workshop_query = _filter_registrations_by_role(Registration.query.filter_by(item_type='workshop'))
    scholarship_query = _filter_registrations_by_role(Registration.query.filter_by(item_type='scholarship'))
    opportunity_query = _filter_registrations_by_role(Registration.query.filter_by(item_type='opportunity'))
    
    counts = {
        'all': all_query.count(),
        'event': event_query.count(),
        'workshop': workshop_query.count(),
        'scholarship': scholarship_query.count(),
        'opportunity': opportunity_query.count()
    }
    
    return render_template('admin/registrations.html', registrations=registrations, counts=counts, selected_type=item_type)

@registrations_bp.route('/export')
@login_required
def export_csv():
    if current_user.role not in ('super_admin', 'college_admin', 'club_president'):
        abort(403)
        
    item_type = request.args.get('type', '')
    query = Registration.query
    if item_type:
        query = query.filter_by(item_type=item_type)
        
    query = _filter_registrations_by_role(query)
    registrations = query.order_by(Registration.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Email', 'Phone', 'Department', 'Year', 'Type', 'Item', 'Message', 'Date'])
    for r in registrations:
        writer.writerow([r.name, r.email, r.phone or '', r.department or '', r.year or '', r.item_type, r.item_title, r.message or '', r.created_at.strftime('%d %b %Y %I:%M %p')])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=registrations_{item_type or "all"}.csv'}
    )

@registrations_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if current_user.role not in ('super_admin', 'college_admin', 'club_president'):
        abort(403)
        
    reg = Registration.query.get_or_404(id)
    
    # Check authorization for club_president
    if current_user.role == 'club_president':
        is_authorized = False
        if reg.item_type == 'event':
            from models.event import Event
            event = Event.query.get(reg.item_id)
            if event and event.club_id == current_user.club_id:
                is_authorized = True
        elif reg.item_type == 'workshop':
            from models.workshop import Workshop
            workshop = Workshop.query.get(reg.item_id)
            if workshop and workshop.created_by == current_user.id:
                is_authorized = True
                
        if not is_authorized:
            flash('Unauthorized action.', 'danger')
            return redirect(url_for('registrations.index'))
            
    db.session.delete(reg)
    db.session.commit()
    flash('Registration entry deleted.', 'success')
    return redirect(url_for('registrations.index'))
