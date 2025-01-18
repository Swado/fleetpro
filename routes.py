from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Truck
import logging
from datetime import datetime

# US states for the dropdown
US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logging.debug(f"Login attempt for username: {username}")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            logging.info(f"User {username} logged in successfully")
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))

        flash('Invalid username or password')
        logging.warning(f"Failed login attempt for username: {username}")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    trucks = Truck.query.filter_by(user_id=current_user.id).all()
    truck_count = len(trucks)
    active_trucks = len([t for t in trucks if t.status == 'active'])
    return render_template('dashboard.html', 
                         trucks=trucks, 
                         truck_count=truck_count,
                         active_trucks=active_trucks)

@app.route('/truck/<int:truck_id>', methods=['GET', 'POST'])
@login_required
def truck_detail(truck_id):
    truck = Truck.query.filter_by(id=truck_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        truck.destination_city = request.form.get('city')
        truck.destination_state = request.form.get('state')
        truck.destination_set_at = datetime.utcnow()
        db.session.commit()
        flash(f'Destination updated for truck {truck.plate_number}')
        return redirect(url_for('truck_detail', truck_id=truck.id))

    return render_template('truck_detail.html', truck=truck, states=US_STATES)