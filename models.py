from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50))  # Font Awesome icon class
    category = db.Column(db.String(50))  # e.g., 'efficiency', 'safety', 'maintenance'
    criteria = db.Column(db.Text)  # JSON string of criteria to earn achievement
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    earned_by = db.relationship('DriverAchievement', back_populates='achievement', overlaps="users")
    users = db.relationship('User', 
                          secondary='driver_achievement',
                          back_populates='achievements',
                          overlaps="driver_achievements,earned_by")

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points_required = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    redeemed_by = db.relationship('DriverReward', back_populates='reward', overlaps="users")
    users = db.relationship('User', 
                          secondary='driver_reward',
                          back_populates='rewards',
                          overlaps="driver_rewards,redeemed_by")

class DriverAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Float, default=0.0)  # Progress towards achievement (0-100)

    user = db.relationship('User', back_populates='driver_achievements', overlaps="achievements,users")
    achievement = db.relationship('Achievement', back_populates='earned_by', overlaps="users")

class DriverReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reward_id = db.Column(db.Integer, db.ForeignKey('reward.id'), nullable=False)
    redeemed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected

    user = db.relationship('User', back_populates='driver_rewards', overlaps="rewards,users")
    reward = db.relationship('Reward', back_populates='redeemed_by', overlaps="users")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    total_distance = db.Column(db.Float, default=0.0)  # Total miles driven
    fuel_efficiency = db.Column(db.Float)  # Average MPG
    safety_score = db.Column(db.Float, default=100.0)  # 0-100 scale
    on_time_delivery_rate = db.Column(db.Float, default=100.0)  # Percentage

    # Fleet management relationships
    trucks = db.relationship('Truck', backref='owner', lazy=True)
    sent_messages = db.relationship('Message',
                                  foreign_keys='Message.sender_id',
                                  backref='sender',
                                  lazy=True)
    received_messages = db.relationship('Message',
                                      foreign_keys='Message.receiver_id',
                                      backref='receiver',
                                      lazy=True)

    # Gamification relationships
    driver_achievements = db.relationship('DriverAchievement', 
                                       back_populates='user',
                                       overlaps="achievements,users")
    driver_rewards = db.relationship('DriverReward', 
                                  back_populates='user',
                                  overlaps="rewards,users")

    achievements = db.relationship('Achievement',
                                secondary='driver_achievement',
                                back_populates='users',
                                overlaps="driver_achievements,earned_by")
    rewards = db.relationship('Reward',
                           secondary='driver_reward',
                           back_populates='users',
                           overlaps="driver_rewards,redeemed_by")

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
    driver_name = db.Column(db.String(100))
    driver_phone = db.Column(db.String(20))
    insurance_expiry = db.Column(db.DateTime)
    current_latitude = db.Column(db.Float)
    current_longitude = db.Column(db.Float)
    trips = db.relationship('TripHistory', backref='truck', lazy=True)

    @property
    def insurance_status(self):
        if not self.insurance_expiry:
            return 'expired'

        days_until_expiry = (self.insurance_expiry - datetime.utcnow()).days
        if days_until_expiry < 0:
            return 'expired'
        elif days_until_expiry <= 30:
            return 'expiring_soon'
        else:
            return 'active'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    message_type = db.Column(db.String(20), default='normal')  # normal or urgent
    subject = db.Column(db.String(100))
    related_truck_id = db.Column(db.Integer, db.ForeignKey('truck.id'))
    related_truck = db.relationship('Truck', backref='messages')

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
    route_deviation = db.Column(db.Float, default=0.0)  # Percentage deviation from suggested route
    scheduled_arrival = db.Column(db.DateTime)  # Expected arrival time
    invoice = db.relationship('Invoice', backref='trip', uselist=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip_history.id'), nullable=False)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled