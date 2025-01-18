from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    trucks = db.relationship('Truck', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')
    last_maintenance = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    destination_city = db.Column(db.String(100))
    destination_state = db.Column(db.String(2))
    destination_set_at = db.Column(db.DateTime)
    trips = db.relationship('TripHistory', backref='truck', lazy=True)

class TripHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'), nullable=False)
    start_city = db.Column(db.String(100), nullable=False)
    start_state = db.Column(db.String(2), nullable=False)
    end_city = db.Column(db.String(100), nullable=False)
    end_state = db.Column(db.String(2), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    distance = db.Column(db.Float)  # in miles
    status = db.Column(db.String(20), default='in_progress')
    runtime_hours = db.Column(db.Float, default=0.0)  # Daily active driving time
    idle_time_hours = db.Column(db.Float, default=0.0)  # Daily idle time
    invoice = db.relationship('Invoice', backref='trip', uselist=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip_history.id'), nullable=False)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled