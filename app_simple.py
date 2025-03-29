from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session, flash, jsonify
import os
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'fleetpulse_secret_key'  # Required for sessions

# User class mock for template compatibility
class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True
        self.level = 2
    
    @property
    def is_active(self):
        return True

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Add current_user to template context
@app.context_processor
def inject_user():
    if session.get('logged_in'):
        return {'current_user': User(1, session.get('username', 'Admin'))}
    return {'current_user': type('obj', (object,), {'is_authenticated': False})}

# Add get_unread_message_count to template context
@app.context_processor
def utility_processor():
    def get_unread_message_count():
        # Mock function for the template
        return 3
    return dict(get_unread_message_count=get_unread_message_count)

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Mock login - in a real app we would validate credentials
        session['logged_in'] = True
        session['username'] = request.form.get('username', 'Admin')
        flash('You have been successfully logged in!', 'success')
        return redirect(url_for('dashboard'))
    
    # GET request
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Create mock data for the dashboard
    trucks = [
        {
            'id': 1,
            'plate_number': 'XPR-1234',
            'model': 'Freightliner Cascadia',
            'year': 2023,
            'status': 'active',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=30),
            'destination_city': 'Chicago',
            'destination_state': 'IL',
            'driver_name': 'John Smith',
            'driver_phone': '+1234567890',
            'trips': [
                {
                    'start_city': 'New York',
                    'start_state': 'NY',
                    'end_city': 'Chicago',
                    'end_state': 'IL',
                    'start_date': datetime.datetime.now() - datetime.timedelta(days=5),
                    'end_date': datetime.datetime.now() - datetime.timedelta(days=3),
                    'distance': 789.5,
                    'status': 'completed',
                    'runtime_hours': 14.2
                }
            ]
        },
        {
            'id': 2,
            'plate_number': 'XPR-5678',
            'model': 'Peterbilt 389',
            'year': 2022,
            'status': 'maintenance',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=60),
            'destination_city': 'Dallas',
            'destination_state': 'TX',
            'driver_name': 'Sarah Johnson',
            'driver_phone': '+1987654321',
            'trips': [
                {
                    'start_city': 'Miami',
                    'start_state': 'FL',
                    'end_city': 'Dallas',
                    'end_state': 'TX',
                    'start_date': datetime.datetime.now() - datetime.timedelta(days=10),
                    'end_date': datetime.datetime.now() - datetime.timedelta(days=7),
                    'distance': 1342.8,
                    'status': 'completed',
                    'runtime_hours': 22.5
                }
            ]
        },
        {
            'id': 3,
            'plate_number': 'XPR-9012',
            'model': 'Kenworth T680',
            'year': 2023,
            'status': 'inactive',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=15),
            'driver_name': 'Michael Brown',
            'driver_phone': '+1122334455',
            'trips': []
        }
    ]
    
    active_trucks = sum(1 for t in trucks if t['status'] == 'active')
    truck_count = len(trucks)
    
    # Show dashboard page with mock data
    return render_template('dashboard.html', 
                          trucks=trucks, 
                          active_trucks=active_trucks, 
                          truck_count=truck_count)

# Route for demo login without form submission
@app.route('/demo-login')
def demo_login():
    session['logged_in'] = True
    session['username'] = 'Demo User'
    flash('You have been logged in with the demo account!', 'success')
    return redirect(url_for('dashboard'))

# Fleet services route
@app.route('/fleet_services')
@login_required
def fleet_services():
    # Mock data for the fleet services page
    insurance_plans = [
        {
            'provider': 'TruckGuard Insurance',
            'rating': 4.8,
            'coverage': 'Comprehensive Fleet Coverage',
            'monthly_premium': 1250.00,
            'deductible': 1000.00,
            'features': [
                'Accident liability up to $2M',
                '24/7 Roadside assistance',
                'Cargo coverage',
                'Medical payments',
                'Uninsured motorist protection'
            ],
            'contact': '(800) 555-1234'
        },
        {
            'provider': 'FreightShield Pro',
            'rating': 4.6,
            'coverage': 'Premium Commercial Coverage',
            'monthly_premium': 1100.00,
            'deductible': 1500.00,
            'features': [
                'Liability coverage up to $1.5M',
                'Physical damage protection',
                'Electronic equipment coverage',
                'Towing and labor',
                'Rental reimbursement'
            ],
            'contact': '(888) 555-5678'
        }
    ]
    
    lawyers = [
        {
            'name': 'Daniel Morgan, Esq.',
            'rating': 4.9,
            'specialization': 'Transportation Law',
            'location': 'Chicago, IL',
            'monthly_rate': 2500.00,
            'response_time': 'Within 2 hours',
            'services': [
                'DOT compliance',
                'Accident litigation',
                'Contract review',
                'Driver employment issues',
                'Insurance claims'
            ],
            'languages': ['English', 'Spanish']
        },
        {
            'name': 'Sarah Johnson, J.D.',
            'rating': 4.7,
            'specialization': 'Commercial Transportation',
            'location': 'Dallas, TX',
            'monthly_rate': 2200.00,
            'response_time': 'Same day',
            'services': [
                'HOS violations',
                'Weight restrictions',
                'FMCSA regulations',
                'State permit issues',
                'Cargo claims'
            ],
            'languages': ['English', 'French']
        }
    ]
    
    payment_data = {
        'driver_payroll': {
            'next_scheduled': 'May 15, 2023',
            'pending_payments': 14,
            'total_pending': 28750.50,
            'early_payment_fee': '1.5%',
            'payment_methods': ['Direct deposit', 'Payment card', 'Bank transfer']
        },
        'repair_invoices': {
            'pending': 8,
            'approved': 12,
            'rejected': 3,
            'total_pending': 12250.75,
            'total_approved': 18750.25,
            'preferred_vendors': ['TruckFix Network', 'MobileMech Services', 'FleetCare Partners']
        },
        'invoice_tracking': {
            'outstanding': 45250.50,
            'processed': 158750.75,
            'overdue': 3250.25,
            'aging_brackets': {
                'Current': 32000.00,
                '1-30 days': 10250.50,
                '31-60 days': 2500.00,
                '61-90 days': 500.00
            }
        }
    }
    
    current_pay_period = 'May 1-15, 2023'
    
    return render_template('fleet_services.html',
                         insurance_plans=insurance_plans,
                         lawyers=lawyers, 
                         payment_data=payment_data,
                         current_pay_period=current_pay_period)

# Messages route
@app.route('/messages')
@login_required
def messages():
    # Mock messages data
    messages = [
        {
            'id': 1,
            'subject': 'Delivery Schedule Update',
            'content': 'Please note that the delivery schedule for next week has been updated. Check the attached document for details.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(hours=3),
            'is_read': False,
            'message_type': 'normal',
            'sender': {'id': 2, 'username': 'Dispatch Manager'},
            'receiver': {'id': 1, 'username': session.get('username', 'Admin')},
            'related_truck_id': 1,
            'related_truck': {'plate_number': 'XPR-1234'}
        },
        {
            'id': 2,
            'subject': 'URGENT: Road Closure Alert',
            'content': 'There is a major road closure on I-95 due to an accident. Please reroute trucks in that area immediately.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=1),
            'is_read': True,
            'message_type': 'urgent',
            'sender': {'id': 3, 'username': 'Safety Officer'},
            'receiver': {'id': 1, 'username': session.get('username', 'Admin')},
            'related_truck_id': None,
            'related_truck': None
        },
        {
            'id': 3,
            'subject': 'Maintenance Request Approved',
            'content': 'The maintenance request for truck XPR-5678 has been approved. Please schedule service at your earliest convenience.',
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=3),
            'is_read': True,
            'message_type': 'normal',
            'sender': {'id': 4, 'username': 'Maintenance Dept'},
            'receiver': {'id': 1, 'username': session.get('username', 'Admin')},
            'related_truck_id': 2,
            'related_truck': {'plate_number': 'XPR-5678'}
        }
    ]
    
    # Mock users for the send message form
    users = [
        {'id': 2, 'username': 'Dispatch Manager'},
        {'id': 3, 'username': 'Safety Officer'},
        {'id': 4, 'username': 'Maintenance Dept'},
        {'id': 5, 'username': 'Fleet Director'}
    ]
    
    # Mock trucks for the related truck dropdown
    trucks = [
        {'id': 1, 'plate_number': 'XPR-1234', 'driver_name': 'John Smith'},
        {'id': 2, 'plate_number': 'XPR-5678', 'driver_name': 'Sarah Johnson'},
        {'id': 3, 'plate_number': 'XPR-9012', 'driver_name': 'Michael Brown'}
    ]
    
    return render_template('messages.html', messages=messages, users=users, trucks=trucks)

# API endpoint to get message details
@app.route('/api/messages/<int:message_id>')
@login_required
def get_message(message_id):
    # Mock message data based on ID
    if message_id == 1:
        message = {
            'subject': 'Delivery Schedule Update',
            'content': 'Please note that the delivery schedule for next week has been updated. Check the attached document for details.',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime('%m/%d/%Y %H:%M'),
            'is_read': False,
            'message_type': 'normal',
            'sender': 'Dispatch Manager',
            'truck': 'XPR-1234'
        }
    elif message_id == 2:
        message = {
            'subject': 'URGENT: Road Closure Alert',
            'content': 'There is a major road closure on I-95 due to an accident. Please reroute trucks in that area immediately.',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%m/%d/%Y %H:%M'),
            'is_read': True,
            'message_type': 'urgent',
            'sender': 'Safety Officer',
            'truck': None
        }
    elif message_id == 3:
        message = {
            'subject': 'Maintenance Request Approved',
            'content': 'The maintenance request for truck XPR-5678 has been approved. Please schedule service at your earliest convenience.',
            'timestamp': (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%m/%d/%Y %H:%M'),
            'is_read': True,
            'message_type': 'normal',
            'sender': 'Maintenance Dept',
            'truck': 'XPR-5678'
        }
    else:
        return jsonify({'error': 'Message not found'}), 404
    
    return jsonify(message)

# API endpoint to mark message as read
@app.route('/api/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_message_read(message_id):
    # In a real app, we would update the database here
    return jsonify({'success': True})

# Send message endpoint
@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    # In a real app, we would save the message to the database
    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('messages'))

# Truck Detail Route
@app.route('/truck/<int:truck_id>')
@login_required
def truck_detail(truck_id):
    # Find the truck by ID in our mock data
    trucks = [
        {
            'id': 1,
            'plate_number': 'XPR-1234',
            'model': 'Freightliner Cascadia',
            'year': 2023,
            'status': 'active',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=30),
            'destination_city': 'Chicago',
            'destination_state': 'IL',
            'driver_name': 'John Smith',
            'driver_phone': '+1234567890',
            'trips': [
                {
                    'id': 101,
                    'start_city': 'New York',
                    'start_state': 'NY',
                    'end_city': 'Chicago',
                    'end_state': 'IL',
                    'start_date': datetime.datetime.now() - datetime.timedelta(days=5),
                    'end_date': datetime.datetime.now() - datetime.timedelta(days=3),
                    'distance': 789.5,
                    'status': 'completed',
                    'runtime_hours': 14.2,
                    'invoice': {
                        'id': 1001,
                        'amount': 2500.00,
                        'status': 'paid'
                    }
                }
            ]
        },
        {
            'id': 2,
            'plate_number': 'XPR-5678',
            'model': 'Peterbilt 389',
            'year': 2022,
            'status': 'maintenance',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=60),
            'destination_city': 'Dallas',
            'destination_state': 'TX',
            'driver_name': 'Sarah Johnson',
            'driver_phone': '+1987654321',
            'trips': [
                {
                    'id': 102,
                    'start_city': 'Miami',
                    'start_state': 'FL',
                    'end_city': 'Dallas',
                    'end_state': 'TX',
                    'start_date': datetime.datetime.now() - datetime.timedelta(days=10),
                    'end_date': datetime.datetime.now() - datetime.timedelta(days=7),
                    'distance': 1342.8,
                    'status': 'completed',
                    'runtime_hours': 22.5,
                    'invoice': {
                        'id': 1002,
                        'amount': 3250.50,
                        'status': 'pending'
                    }
                }
            ]
        },
        {
            'id': 3,
            'plate_number': 'XPR-9012',
            'model': 'Kenworth T680',
            'year': 2023,
            'status': 'inactive',
            'last_maintenance': datetime.datetime.now() - datetime.timedelta(days=15),
            'driver_name': 'Michael Brown',
            'driver_phone': '+1122334455',
            'trips': []
        }
    ]
    
    # Find the truck in our mock data
    truck = next((t for t in trucks if t['id'] == truck_id), None)
    if not truck:
        flash('Truck not found!', 'error')
        return redirect(url_for('dashboard'))
    
    # US state abbreviations for the form dropdown
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    
    return render_template('truck_detail.html', truck=truck, states=states)

# API endpoint for truck performance data
@app.route('/api/truck/<int:truck_id>/performance')
@login_required
def truck_performance(truck_id):
    # Mock performance data
    labels = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 11", "Week 12"]
    runtime_data = [42, 38, 45, 40, 43, 32, 37, 44, 40, 41, 38, 42]
    idle_data = [8, 12, 6, 10, 7, 15, 11, 6, 10, 9, 11, 8]
    
    return jsonify({
        'labels': labels,
        'datasets': [
            {
                'label': 'Active Runtime (hours)',
                'data': runtime_data,
                'backgroundColor': 'rgba(46, 204, 113, 0.5)',
                'borderColor': 'rgba(46, 204, 113, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Idle Time (hours)',
                'data': idle_data,
                'backgroundColor': 'rgba(231, 76, 60, 0.5)',
                'borderColor': 'rgba(231, 76, 60, 1)',
                'borderWidth': 1
            }
        ]
    })

# AI route suggestion API
@app.route('/api/truck/<int:truck_id>/route-suggestion', methods=['POST'])
@login_required
def get_ai_route_suggestion(truck_id):
    # Mock AI route suggestion data
    start_city = request.form.get('start_city', '')
    start_state = request.form.get('start_state', '')
    destination_city = request.form.get('destination_city', '')
    destination_state = request.form.get('destination_state', '')
    
    # Generate a mock AI response
    suggestion = f"""
    <div class="ai-suggestion">
        <div class="recommendation-header">
            <i class="fas fa-map-marked-alt"></i> <strong>Optimal Route: {start_city}, {start_state} to {destination_city}, {destination_state}</strong>
        </div>
        <div class="recommendation-details">
            <p><strong>Estimated Distance:</strong> 782 miles</p>
            <p><strong>Estimated Travel Time:</strong> 14 hours 30 minutes</p>
            <p><strong>Recommended Stops:</strong></p>
            <ul>
                <li>Rest Area #42 (I-80, mile marker 252) - After 4 hours</li>
                <li>Truck Haven Plaza (I-80, exit 315) - After 9 hours</li>
            </ul>
            
            <div class="weather-warning">
                <i class="fas fa-exclamation-triangle"></i> <strong>Weather Alert:</strong> Heavy rain expected along I-80 corridor between exits 200-300 tomorrow morning.
            </div>
            
            <p><strong>Traffic Information:</strong> Construction zone on I-76 between exits 45-60 causing 30 minute delays. Recommend using I-80 East to I-283 South as an alternative.</p>
            
            <div class="fuel-info">
                <p><strong>Fuel Efficiency:</strong> Maintaining 60-65 mph speed would optimize fuel consumption for this route.</p>
                <p><strong>Recommended Refueling:</strong> TA Travel Center (Exit 310 on I-80) offers the best diesel prices along the route.</p>
            </div>
        </div>
    </div>
    """
    
    return jsonify({
        'success': True,
        'suggestion': suggestion
    })

# AI performance analysis API
@app.route('/api/truck/<int:truck_id>/performance-analysis')
@login_required
def get_ai_performance_analysis(truck_id):
    # Mock AI performance analysis
    analysis = f"""
    <div class="ai-analysis">
        <div class="analysis-header">
            <i class="fas fa-chart-line"></i> <strong>Performance Analysis for Truck #{truck_id}</strong>
        </div>
        <div class="analysis-summary">
            <p>Based on the last 90 days of operation, this truck's performance is <strong class="text-success">12% above fleet average</strong>.</p>
        </div>
        <div class="analysis-metrics">
            <div class="metric-group">
                <h6><i class="fas fa-gas-pump"></i> Fuel Efficiency</h6>
                <p>Average MPG: <strong>6.8 mpg</strong> (Fleet Average: 6.2 mpg)</p>
                <p class="recommendation">Recommendation: Current driving patterns show optimal fuel usage. Continue current practices.</p>
            </div>
            <div class="metric-group">
                <h6><i class="fas fa-clock"></i> Idle Time</h6>
                <p>Average Idle Time: <strong>9.8%</strong> (Fleet Average: 12.5%)</p>
                <p class="recommendation">Recommendation: Excellent idle management. Consider sharing best practices with other drivers.</p>
            </div>
            <div class="metric-group">
                <h6><i class="fas fa-tachometer-alt"></i> Speed Management</h6>
                <p>Time Over 65mph: <strong>18.2%</strong> (Fleet Average: 22.7%)</p>
                <p class="recommendation">Recommendation: Good speed management contributes to fuel savings and reduced wear.</p>
            </div>
            <div class="metric-group">
                <h6><i class="fas fa-wrench"></i> Maintenance Prediction</h6>
                <p>Next Service: <strong>Recommended in 4,200 miles</strong></p>
                <p class="warning"><i class="fas fa-exclamation-circle"></i> Warning: Brake wear indicators suggest service may be needed sooner than scheduled.</p>
                <p class="recommendation">Recommendation: Schedule brake inspection within the next 2 weeks.</p>
            </div>
        </div>
    </div>
    """
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

# Handle specific route patterns for remaining routes
@app.route('/map/<truck_id>')
@app.route('/call/<truck_id>')
@app.route('/services/<service_type>')
@app.route('/fleet')
@app.route('/routes')
@app.route('/drivers')
@app.route('/maintenance')
@app.route('/analytics')
@app.route('/settings')
@app.route('/achievements')
@app.route('/nextload_page')
@login_required
def handle_app_routes(truck_id=None, service_type=None):
    # For now, all routes simply return the preview.html page
    return send_from_directory('.', 'preview.html')

@app.route('/logout')
def logout():
    # Remove session data
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('index'))

# Static file serving routes
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)