from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Truck, TripHistory
import logging
from datetime import datetime, timedelta
from sqlalchemy import func

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


@app.route('/api/truck/<int:truck_id>/performance')
@login_required
def truck_performance(truck_id):
    # Get data for last 90 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    # Query trips for the truck within date range
    trips = TripHistory.query.filter(
        TripHistory.truck_id == truck_id,
        TripHistory.start_date >= start_date,
        TripHistory.start_date <= end_date
    ).all()

    # Prepare data for chart
    dates = []
    runtime_data = []
    idle_time_data = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        dates.append(date_str)

        # Get trips for current date
        day_trips = [t for t in trips if t.start_date.date() == current_date.date()]

        # Calculate averages for the day
        if day_trips:
            avg_runtime = sum(t.runtime_hours for t in day_trips) / len(day_trips)
            avg_idle = sum(t.idle_time_hours for t in day_trips) / len(day_trips)
        else:
            avg_runtime = 0
            avg_idle = 0

        runtime_data.append(round(avg_runtime, 2))
        idle_time_data.append(round(avg_idle, 2))

        current_date += timedelta(days=1)

    return jsonify({
        'dates': dates,
        'runtime': runtime_data,
        'idle_time': idle_time_data
    })