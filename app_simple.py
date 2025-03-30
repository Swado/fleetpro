from flask import Flask, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'preview.html')

# Handle specific route patterns
@app.route('/map/<truck_id>')
@app.route('/call/<truck_id>')
@app.route('/truck/<truck_id>')
@app.route('/services/<service_type>')
@app.route('/dashboard')
@app.route('/fleet')
@app.route('/routes')
@app.route('/drivers')
@app.route('/maintenance')
@app.route('/analytics')
@app.route('/messages')
@app.route('/settings')
def handle_app_routes(truck_id=None, service_type=None):
    # For now, all routes simply return the preview.html page
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