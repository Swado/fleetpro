import os
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify, session, Response, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Truck, TripHistory, Message
from services.ai_service import AIFleetAssistant
from services.gmail_service import gmail_service
import logging
from sqlalchemy import func
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests
import random

ai_assistant = AIFleetAssistant()

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
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            session['is_demo'] = False
            # Initialize email notification status
            session['email_enabled'] = False
            logging.info(f"User {username} logged in successfully")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        flash('Invalid username or password')
        logging.warning(f"Failed login attempt for username: {username}")

    return render_template('login.html')

@app.route('/demo')
def demo_login():
    # Find or create demo user with sample data
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@example.com'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()

        # Add sample trucks for demo user
        from create_test_data import add_trucks_for_user
        add_trucks_for_user('demo', num_trucks=5)

    login_user(demo_user)
    session['is_demo'] = True
    flash('Welcome to the demo! Feel free to explore all features.')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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

    if request.method == 'POST' and not session.get('is_demo'):
        truck.destination_city = request.form.get('city')
        truck.destination_state = request.form.get('state')
        truck.destination_set_at = datetime.utcnow()
        db.session.commit()

        # Send email notification for destination update
        if not session.get('is_demo'):
            email_body = f"""
            Destination Updated for Truck {truck.plate_number}

            New Destination: {truck.destination_city}, {truck.destination_state}
            Update Time: {truck.destination_set_at}

            Truck Details:
            - Model: {truck.model}
            - Year: {truck.year}
            - Status: {truck.status}
            """
            gmail_service.send_email(
                to=current_user.email,
                subject=f"Destination Update - Truck {truck.plate_number}",
                body=email_body
            )

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

@app.route('/api/truck/<int:truck_id>/ai/route-suggestion', methods=['POST'])
@login_required
def get_ai_route_suggestion(truck_id):
    truck = Truck.query.filter_by(id=truck_id, user_id=current_user.id).first_or_404()

    data = request.json
    start_city = data.get('start_city')
    start_state = data.get('start_state')
    destination_city = data.get('destination_city')
    destination_state = data.get('destination_state')

    truck_data = {
        'model': truck.model,
        'last_maintenance': truck.last_maintenance.strftime('%Y-%m-%d'),
        'status': truck.status
    }

    suggestion = ai_assistant.get_route_suggestion(
        start_city, start_state,
        destination_city, destination_state,
        truck_data
    )

    return jsonify({'suggestion': suggestion})

@app.route('/api/truck/<int:truck_id>/ai/performance-analysis')
@login_required
def get_ai_performance_analysis(truck_id):
    # Get last 30 days of data
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)

    trips = TripHistory.query.filter(
        TripHistory.truck_id == truck_id,
        TripHistory.start_date >= start_date
    ).all()

    performance_data = {
        'avg_runtime': sum(t.runtime_hours for t in trips) / len(trips) if trips else 0,
        'avg_idle_time': sum(t.idle_time_hours for t in trips) / len(trips) if trips else 0,
        'total_trips': len(trips)
    }

    analysis = ai_assistant.analyze_performance(performance_data)
    return jsonify({'analysis': analysis})

@app.route('/oauth2callback')
def oauth2callback():
    try:
        logging.info("Starting OAuth callback process")

        # Verify required environment variables
        if not os.environ.get('GMAIL_CLIENT_ID') or not os.environ.get('GMAIL_CLIENT_SECRET'):
            logging.error("Missing Gmail API credentials")
            flash('Email notification setup failed: Missing API credentials')
            return redirect(url_for('dashboard'))

        # Get the authorization URL
        auth_url = gmail_service.authenticate()

        # If we got an auth URL, redirect to it
        if isinstance(auth_url, str):
            return redirect(auth_url)

        # If authentication was successful
        session['email_enabled'] = True
        flash('Email notifications have been successfully enabled.')
        logging.info("Gmail authentication successful")

    except Exception as e:
        logging.error(f"OAuth callback error: {e}", exc_info=True)
        session['email_enabled'] = False
        flash('An error occurred during email setup.')

    return redirect(url_for('dashboard'))


@app.route('/messages')
@login_required
def messages():
    # Get all messages for the current user (both sent and received)
    received_messages = Message.query.filter_by(receiver_id=current_user.id)\
        .order_by(Message.timestamp.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id)\
        .order_by(Message.timestamp.desc()).all()

    # Get all users for the new message form
    users = User.query.filter(User.id != current_user.id).all()
    # Get all trucks for the current user
    trucks = Truck.query.filter_by(user_id=current_user.id).all()

    return render_template('messages.html', 
                         messages=received_messages + sent_messages,
                         users=users,
                         trucks=trucks)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    try:
        new_message = Message(
            sender_id=current_user.id,
            receiver_id=request.form['receiver_id'],
            subject=request.form['subject'],
            content=request.form['content'],
            message_type=request.form['message_type'],
            related_truck_id=request.form['related_truck_id'] or None
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent successfully')
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        flash('Error sending message')
        db.session.rollback()

    return redirect(url_for('messages'))

@app.route('/api/messages/<int:message_id>')
@login_required
def get_message(message_id):
    message = Message.query.get_or_404(message_id)

    # Security check - only sender and receiver can view the message
    if message.sender_id != current_user.id and message.receiver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'id': message.id,
        'subject': message.subject,
        'content': message.content,
        'sender': message.sender.username,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
        'is_read': message.is_read,
        'message_type': message.message_type,
        'truck': f"{message.related_truck.plate_number} - {message.related_truck.driver_name}" if message.related_truck else None
    })

@app.route('/api/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    message = Message.query.get_or_404(message_id)

    # Security check - only receiver can mark as read
    if message.receiver_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    message.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.context_processor
def utility_processor():
    def get_unread_message_count():
        if current_user.is_authenticated:
            return Message.query.filter_by(
                receiver_id=current_user.id,
                is_read=False
            ).count()
        return 0

    return dict(get_unread_message_count=get_unread_message_count)

@app.route('/fleet-services')
@login_required
def fleet_services():
    # Test data for insurance plans
    insurance_plans = [
        {
            'provider': 'SafeFleet Insurance Co.',
            'coverage': 'Comprehensive Commercial Fleet Coverage',
            'monthly_premium': 1250.00,
            'deductible': 1000.00,
            'features': ['24/7 Roadside Assistance', 'Cargo Protection', 'Liability Coverage'],
            'rating': 4.8,
            'contact': 'John Smith (866) 555-0123'
        },
        {
            'provider': 'TruckGuard Insurance',
            'coverage': 'Premium Fleet Protection Plus',
            'monthly_premium': 1450.00,
            'deductible': 750.00,
            'features': ['Accident Forgiveness', 'Medical Payments', 'Property Damage'],
            'rating': 4.6,
            'contact': 'Mary Johnson (866) 555-0124'
        },
        {
            'provider': 'FleetSecure Partners',
            'coverage': 'Ultimate Fleet Shield',
            'monthly_premium': 1650.00,
            'deductible': 500.00,
            'features': ['Full Gap Coverage', 'New Vehicle Replacement', 'Personal Injury Protection'],
            'rating': 4.9,
            'contact': 'Robert Davis (866) 555-0125'
        }
    ]

    # Test data for legal support
    lawyers = [
        {
            'name': 'Johnson & Associates',
            'specialization': 'Transportation Law',
            'location': 'Chicago, IL',
            'monthly_rate': 2500.00,
            'services': ['Accident Defense', 'Regulatory Compliance', 'Driver Rights'],
            'rating': 4.9,
            'response_time': '15 minutes',
            'languages': ['English', 'Spanish']
        },
        {
            'name': 'Freeman Legal Group',
            'specialization': 'Commercial Fleet Defense',
            'location': 'Dallas, TX',
            'monthly_rate': 2200.00,
            'services': ['Insurance Claims', 'Contract Disputes', 'Employment Law'],
            'rating': 4.7,
            'response_time': '30 minutes',
            'languages': ['English', 'Chinese']
        }
    ]

    # Test data for payments and invoices
    current_pay_period = f"{datetime.now().strftime('%B %d')} - {(datetime.now() + timedelta(days=14)).strftime('%B %d, %Y')}"
    next_payment_date = (datetime.now() + timedelta(days=7)).strftime('%B %d, %Y')

    payment_data = {
        'driver_payroll': {
            'pending_payments': 12,
            'total_pending': 35000.00,
            'early_payment_fee': '1.5%',
            'next_scheduled': next_payment_date,
            'payment_methods': ['Direct Deposit', 'PayPal', 'Wire Transfer']
        },
        'repair_invoices': {
            'pending': 5,
            'approved': 8,
            'rejected': 2,
            'total_pending': 12000.00,
            'total_approved': 18000.00,
            'preferred_vendors': ['National Truck Service', 'FleetFix Pro', 'Diesel Doctors']
        },
        'invoice_tracking': {
            'outstanding': 8500.00,
            'processed': 35000.00,
            'overdue': 4500.00,
            'aging_brackets': {
                '0-30 days': 5000.00,
                '31-60 days': 2500.00,
                '61-90 days': 1500.00,
                '90+ days': 1000.00
            }
        }
    }

    return render_template('fleet_services.html',
                         insurance_plans=insurance_plans,
                         lawyers=lawyers,
                         current_pay_period=current_pay_period,
                         next_payment_date=next_payment_date,
                         payment_data=payment_data)

@app.route('/add_sample_trips')
@login_required
def add_sample_trips():
    if not session.get('is_demo'):
        trucks = Truck.query.filter_by(user_id=current_user.id).all()
        states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
        cities = {
            'CA': ['Los Angeles', 'San Francisco', 'San Diego'],
            'TX': ['Houston', 'Dallas', 'Austin'],
            'FL': ['Miami', 'Orlando', 'Tampa'],
            'NY': ['New York City', 'Buffalo', 'Albany'],
            'IL': ['Chicago', 'Springfield', 'Rockford']
        }

        for truck in trucks:
            # Add 5 sample trips for each truck
            for _ in range(5):
                start_state = random.choice(states)
                end_state = random.choice(states)

                start_city = random.choice(cities.get(start_state, ['City 1', 'City 2', 'City 3']))
                end_city = random.choice(cities.get(end_state, ['City 1', 'City 2', 'City 3']))

                start_date = datetime.now() - timedelta(days=random.randint(1, 90))

                trip = TripHistory(
                    truck_id=truck.id,
                    start_city=start_city,
                    start_state=start_state,
                    end_city=end_city,
                    end_state=end_state,
                    start_date=start_date,
                    end_date=start_date + timedelta(days=random.randint(1, 5)),
                    status=random.choice(['completed', 'in_progress']),
                    distance=random.uniform(100, 1000),
                    runtime_hours=random.uniform(10, 50),
                    idle_time_hours=random.uniform(2, 10)
                )
                db.session.add(trip)

        db.session.commit()
        flash('Sample trips added successfully')

    return redirect(url_for('dashboard'))