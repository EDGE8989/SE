from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.registration import Registration

registration_bp = Blueprint('registration', __name__, url_prefix='/register')

@registration_bp.route('/<item_type>/<int:item_id>', methods=['GET', 'POST'])
def register(item_type, item_id):
    # Validate item_type
    if item_type not in ('event', 'workshop', 'scholarship', 'opportunity'):
        flash('Invalid registration type.', 'danger')
        return redirect(url_for('public.home'))
    
    # Get the item details
    item = None
    if item_type == 'event':
        from models.event import Event
        item = Event.query.get_or_404(item_id)
    elif item_type == 'workshop':
        from models.workshop import Workshop
        item = Workshop.query.get_or_404(item_id)
    elif item_type == 'scholarship':
        from models.scholarship import Scholarship
        item = Scholarship.query.get_or_404(item_id)
    elif item_type == 'opportunity':
        from models.opportunity import Opportunity
        item = Opportunity.query.get_or_404(item_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department = request.form.get('department')
        year = request.form.get('year')
        message = request.form.get('message')
        
        # Check for duplicate registration
        existing = Registration.query.filter_by(
            email=email, item_type=item_type, item_id=item_id
        ).first()
        if existing:
            flash('You have already registered for this!', 'warning')
            return redirect(url_for('registration.register', item_type=item_type, item_id=item_id))
        
        registration = Registration(
            name=name,
            email=email,
            phone=phone,
            department=department,
            year=year,
            item_type=item_type,
            item_id=item_id,
            item_title=item.title,
            message=message
        )
        
        db.session.add(registration)
        db.session.commit()
        
        flash(f'Successfully registered for {item.title}!', 'success')
        return redirect(url_for('registration.success', item_type=item_type, item_id=item_id))
    
    return render_template('public/register.html', item=item, item_type=item_type)

@registration_bp.route('/<item_type>/<int:item_id>/success')
def success(item_type, item_id):
    item = None
    if item_type == 'event':
        from models.event import Event
        item = Event.query.get_or_404(item_id)
    elif item_type == 'workshop':
        from models.workshop import Workshop
        item = Workshop.query.get_or_404(item_id)
    elif item_type == 'scholarship':
        from models.scholarship import Scholarship
        item = Scholarship.query.get_or_404(item_id)
    elif item_type == 'opportunity':
        from models.opportunity import Opportunity
        item = Opportunity.query.get_or_404(item_id)
    
    return render_template('public/register_success.html', item=item, item_type=item_type)
