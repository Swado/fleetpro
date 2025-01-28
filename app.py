import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
import urllib.parse

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_only_for_development"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        from models import User
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid email or password')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    from models import Truck, Message
    trucks = Truck.query.filter_by(user_id=current_user.id).all()
    active_trucks = len([t for t in trucks if t.status == 'active'])
    unread_messages = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    return render_template('dashboard.html', 
                         trucks=trucks,
                         active_trucks=active_trucks,
                         truck_count=len(trucks),
                         unread_count=unread_messages)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

with app.app_context():
    # Import models after app creation to avoid circular imports
    from models import User, Truck, Message
    db.create_all()

    def create_admin_user():
        try:
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                logging.info("Admin user created successfully")
            else:
                logging.info("Admin user already exists")
        except Exception as e:
            logging.error(f"Error creating admin user: {e}")
            db.session.rollback()

    create_admin_user()