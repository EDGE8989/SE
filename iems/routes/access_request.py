from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.access_request import AccessRequest
from models.club import Club

access_request_bp = Blueprint('access_request', __name__, url_prefix='/request-access')

@access_request_bp.route('/', methods=['GET', 'POST'])
def apply():
    clubs = Club.query.filter_by(is_active=True).order_by(Club.name.asc()).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        requested_role = request.form.get('requested_role', '').strip()
        designation = request.form.get('designation', '').strip()
        club_id = request.form.get('club_id') or None
        club_name = request.form.get('club_name', '').strip()
        reason = request.form.get('reason', '').strip()

        if not name or not email or not requested_role or not reason:
            flash('Please fill in all required fields.', 'danger')
            return render_template('public/request_access.html', clubs=clubs)

        # Check if a pending request already exists for this email
        existing = AccessRequest.query.filter_by(email=email, status='pending').first()
        if existing:
            flash('A pending access request already exists for this email address. Please wait for admin review.', 'warning')
            return redirect(url_for('access_request.apply'))

        # Check if email is already a registered user
        from models.user import User
        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists. Please contact the administrator.', 'warning')
            return redirect(url_for('access_request.apply'))

        access_req = AccessRequest(
            name=name,
            email=email,
            phone=phone,
            requested_role=requested_role,
            designation=designation,
            club_id=int(club_id) if club_id else None,
            club_name=club_name if not club_id else None,
            reason=reason
        )

        db.session.add(access_req)
        db.session.commit()

        flash('Your access request has been submitted! The admin team will review it and contact you at your email.', 'success')
        return redirect(url_for('access_request.request_submitted'))

    return render_template('public/request_access.html', clubs=clubs)

@access_request_bp.route('/submitted')
def request_submitted():
    return render_template('public/request_submitted.html')
