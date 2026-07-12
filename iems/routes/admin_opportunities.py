from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.opportunity import Opportunity
from utils.decorators import role_required
from utils.helpers import log_activity
from datetime import datetime

opportunities_bp = Blueprint('opportunities', __name__, url_prefix='/admin/opportunities')

@opportunities_bp.route('/')
@login_required
@role_required('super_admin', 'college_admin')
def index():
    opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    return render_template('admin/opportunities.html', opportunities=opportunities)

@opportunities_bp.route('/add', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def add():
    title = request.form.get('title')
    company = request.form.get('company')
    opp_type = request.form.get('type')
    description = request.form.get('description')
    location = request.form.get('location')
    stipend = request.form.get('stipend')
    deadline_str = request.form.get('deadline')
    application_link = request.form.get('application_link')
    
    deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
    
    opportunity = Opportunity(
        title=title,
        company=company,
        type=opp_type,
        description=description,
        location=location,
        stipend=stipend,
        deadline=deadline_obj,
        application_link=application_link
    )
    
    db.session.add(opportunity)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_OPPORTUNITY', 'Opportunities', f'Created {opp_type}: {title} at {company}')
    flash('Opportunity added successfully!', 'success')
    return redirect(url_for('opportunities.index'))

@opportunities_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def delete(id):
    opportunity = Opportunity.query.get_or_404(id)
    title = opportunity.title
    db.session.delete(opportunity)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_OPPORTUNITY', 'Opportunities', f'Deleted opportunity: {title}')
    flash('Opportunity deleted successfully.', 'success')
    return redirect(url_for('opportunities.index'))
