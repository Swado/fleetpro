import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

# create the app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_only_for_development"

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    parsed = urllib.parse.urlparse(database_url)
    if parsed.password:
        database_url = database_url.replace(parsed.password, urllib.parse.quote(parsed.password))

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Register the utility function for templates before importing routes
def get_unread_message_count():
    if not current_user.is_authenticated:
        return 0
    try:
        from models import Message
        return Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    except Exception:
        return 0

app.jinja_env.globals.update(get_unread_message_count=get_unread_message_count)

# Import models after initializing extensions
from models import User, Truck, Message, TripHistory

with app.app_context():
    try:
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully")

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
                    logger.info("Admin user created successfully")
                else:
                    logger.info("Admin user already exists")
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
                db.session.rollback()

        create_admin_user()
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")

# Import routes after initializing everything else
import routes  # noqa: F401

# Static file serving routes
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

@app.route('/static/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'audio'),
        filename,
        mimetype='audio/mpeg'
    )