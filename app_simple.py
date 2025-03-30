from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'landing.html')

@app.route('/login')
def login():
    return send_from_directory('.', 'login.html')

# Handle specific route patterns
@app.route('/map/<truck_id>')
def map_view(truck_id):
    return send_from_directory('.', 'map_view.html')

@app.route('/call/<truck_id>')
def call_driver(truck_id):
    return send_from_directory('.', 'call_driver.html')

@app.route('/truck/<truck_id>')
def truck_detail(truck_id):
    return send_from_directory('.', 'truck_detail.html')

@app.route('/services/<service_type>')
def services(service_type):
    return send_from_directory('.', 'services.html')

@app.route('/dashboard')
@app.route('/fleet')
@app.route('/routes')
@app.route('/drivers')
@app.route('/maintenance')
@app.route('/analytics')
@app.route('/messages')
@app.route('/settings')
def handle_app_routes():
    # For most routes, return the main dashboard
    return send_from_directory('.', 'preview.html')

@app.route('/logout')
def logout():
    # In a real app, this would destroy the session
    # For now, just redirect to the main page
    return redirect(url_for('index'))

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)