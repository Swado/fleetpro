import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_only_for_development"

# Database configuration
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

with app.app_context():
    try:
        # Import models after app creation to avoid circular imports
        from models import User, Truck, Message, TripHistory
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

# Register the utility function for templates
def get_unread_message_count():
    if not current_user.is_authenticated:
        return 0
    from models import Message
    return Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()

app.jinja_env.globals.update(get_unread_message_count=get_unread_message_count)

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files with correct content type"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'audio'),
        filename,
        mimetype='audio/mpeg'
    )