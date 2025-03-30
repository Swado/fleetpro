from flask import Flask, render_template, send_from_directory, redirect, url_for, request, session
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, 
            static_folder='static',
            template_folder='.')

# Secret key for session
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fleetpulse_secret_key')

# Sample user data for demo purposes
users = {
    'admin': {
        'password': 'admin123',
        'name': 'Admin User',
        'role': 'admin'
    }
}

# Sample truck data
trucks = [
    {
        'id': 1,
        'driver_name': 'John Smith',
        'plate_number': 'IL-7845TK',
        'model': 'Freightliner Cascadia',
        'year': 2023,
        'status': 'active',
        'driver_phone': '(312) 555-7890',
        'current_city': 'Ogallala',
        'current_state': 'NE',
        'destination_city': 'Denver',
        'destination_state': 'CO'
    },
    {
        'id': 2,
        'driver_name': 'Sarah Johnson',
        'plate_number': 'TX-9273LP',
        'model': 'Kenworth T680',
        'year': 2022,
        'status': 'active',
        'driver_phone': '(214) 555-3421',
        'current_city': 'Oklahoma City',
        'current_state': 'OK',
        'destination_city': 'San Antonio',
        'destination_state': 'TX'
    },
    {
        'id': 3,
        'driver_name': 'Michael Brown',
        'plate_number': 'CA-5591RK',
        'model': 'Peterbilt 579',
        'year': 2021,
        'status': 'inactive',
        'driver_phone': '(415) 555-8876',
        'current_city': 'Las Vegas',
        'current_state': 'NV',
        'destination_city': 'Los Angeles',
        'destination_state': 'CA'
    },
    {
        'id': 4,
        'driver_name': 'Emily Davis',
        'plate_number': 'GA-3378TJ',
        'model': 'Volvo VNL 860',
        'year': 2023,
        'status': 'active',
        'driver_phone': '(404) 555-2249',
        'current_city': 'Nashville',
        'current_state': 'TN',
        'destination_city': 'Atlanta',
        'destination_state': 'GA'
    },
    {
        'id': 5,
        'driver_name': 'David Wilson',
        'plate_number': 'OH-6734KP',
        'model': 'Mack Anthem',
        'year': 2022,
        'status': 'active',
        'driver_phone': '(614) 555-9082',
        'current_city': 'Indianapolis',
        'current_state': 'IN',
        'destination_city': 'Columbus',
        'destination_state': 'OH'
    },
    {
        'id': 6,
        'driver_name': 'Jennifer Lee',
        'plate_number': 'WA-2209TS',
        'model': 'International LT',
        'year': 2023,
        'status': 'active',
        'driver_phone': '(206) 555-4433',
        'current_city': 'Portland',
        'current_state': 'OR',
        'destination_city': 'Seattle',
        'destination_state': 'WA'
    },
    {
        'id': 7,
        'driver_name': 'Robert Martinez',
        'plate_number': 'FL-8867MP',
        'model': 'Western Star 5700',
        'year': 2021,
        'status': 'inactive',
        'driver_phone': '(305) 555-1156',
        'current_city': 'Orlando',
        'current_state': 'FL',
        'destination_city': 'Miami',
        'destination_state': 'FL'
    },
    {
        'id': 8,
        'driver_name': 'Lisa Thompson',
        'plate_number': 'NY-3342RS',
        'model': 'Freightliner Cascadia',
        'year': 2022,
        'status': 'active',
        'driver_phone': '(212) 555-6698',
        'current_city': 'Pittsburgh',
        'current_state': 'PA',
        'destination_city': 'New York',
        'destination_state': 'NY'
    },
    {
        'id': 9,
        'driver_name': 'Daniel White',
        'plate_number': 'AZ-1173KL',
        'model': 'Kenworth T680',
        'year': 2023,
        'status': 'active',
        'driver_phone': '(602) 555-3377',
        'current_city': 'Albuquerque',
        'current_state': 'NM',
        'destination_city': 'Phoenix',
        'destination_state': 'AZ'
    },
    {
        'id': 10,
        'driver_name': 'Jessica Harris',
        'plate_number': 'MI-5528TG',
        'model': 'Peterbilt 389',
        'year': 2022,
        'status': 'active',
        'driver_phone': '(313) 555-9944',
        'current_city': 'Chicago',
        'current_state': 'IL',
        'destination_city': 'Detroit',
        'destination_state': 'MI'
    }
]


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/dispatch')
        else:
            error = 'Invalid credentials. Please try again.'
    
    return send_from_directory('.', 'login.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username]['password'] == password:
        session['logged_in'] = True
        session['username'] = username
        return redirect('/dispatch')
    else:
        return redirect('/login')


@app.route('/dispatch')
def dispatch():
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'dispatch.html')


@app.route('/map_view/<int:truck_id>')
def map_view(truck_id):
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'map_view.html')


@app.route('/call_driver/<int:truck_id>')
def call_driver(truck_id):
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'call_driver.html')


@app.route('/truck_detail/<int:truck_id>')
def truck_detail(truck_id):
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'truck_detail.html')


@app.route('/services/<service_type>')
def services(service_type):
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'services.html')


@app.route('/services')
def services_main():
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('.', 'services.html')


@app.route('/api/trucks')
def handle_app_routes():
    if not session.get('logged_in'):
        return {'error': 'Not authenticated'}, 401
    return {'trucks': trucks}


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect('/login')


@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)