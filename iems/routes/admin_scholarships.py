from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.scholarship import Scholarship
from utils.decorators import role_required
from utils.helpers import log_activity
from datetime import datetime

scholarships_bp = Blueprint('scholarships', __name__, url_prefix='/admin/scholarships')

@scholarships_bp.route('/')
@login_required
@role_required('super_admin', 'college_admin')
def index():
    scholarships = Scholarship.query.order_by(Scholarship.created_at.desc()).all()
    return render_template('admin/scholarships.html', scholarships=scholarships)

@scholarships_bp.route('/add', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    eligibility = request.form.get('eligibility')
    amount = request.form.get('amount')
    deadline_str = request.form.get('deadline')
    application_link = request.form.get('application_link')
    
    deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None
    
    scholarship = Scholarship(
        title=title,
        description=description,
        eligibility=eligibility,
        amount=amount,
        deadline=deadline_obj,
        application_link=application_link
    )
    
    db.session.add(scholarship)
    db.session.commit()
    
    log_activity(current_user.id, 'CREATE_SCHOLARSHIP', 'Scholarships', f'Created scholarship: {title}')
    flash('Scholarship added successfully!', 'success')
    return redirect(url_for('scholarships.index'))

@scholarships_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('super_admin', 'college_admin')
def delete(id):
    scholarship = Scholarship.query.get_or_404(id)
    title = scholarship.title
    db.session.delete(scholarship)
    db.session.commit()
    log_activity(current_user.id, 'DELETE_SCHOLARSHIP', 'Scholarships', f'Deleted scholarship: {title}')
    flash('Scholarship deleted successfully.', 'success')
    return redirect(url_for('scholarships.index'))
