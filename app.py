import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

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

def create_admin_user():
    from models import User
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

with app.app_context():
    import models
    db.create_all()
    create_admin_user()

from routes import *