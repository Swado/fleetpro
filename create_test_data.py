from app import app, db
from models import User
from datetime import datetime, timedelta
import random

# Sample data for random generation
TRUCK_MODELS = [
    "Freightliner Cascadia", "Peterbilt 579", "Kenworth T680",
    "Volvo VNL", "Mack Anthem", "International LT"
]

TRUCK_STATUSES = ["active", "maintenance", "inactive"]

DRIVER_NAMES = [
    "John Smith", "Maria Garcia", "David Johnson", "James Wilson",
    "Sarah Brown", "Michael Davis", "Robert Miller", "Lisa Anderson",
    "William Taylor", "Jennifer Martinez"
]

# Sample locations across the US
SAMPLE_LOCATIONS = [
    {"city": "Los Angeles", "state": "CA", "lat": 34.0522, "lon": -118.2437},
    {"city": "New York", "state": "NY", "lat": 40.7128, "lon": -74.0060},
    {"city": "Chicago", "state": "IL", "lat": 41.8781, "lon": -87.6298},
    {"city": "Houston", "state": "TX", "lat": 29.7604, "lon": -95.3698},
    {"city": "Phoenix", "state": "AZ", "lat": 33.4484, "lon": -112.0740},
    {"city": "San Francisco", "state": "CA", "lat": 37.7749, "lon": -122.4194},
    {"city": "Miami", "state": "FL", "lat": 25.7617, "lon": -80.1918},
    {"city": "Seattle", "state": "WA", "lat": 47.6062, "lon": -122.3321},
    {"city": "Denver", "state": "CO", "lat": 39.7392, "lon": -104.9903},
    {"city": "Atlanta", "state": "GA", "lat": 33.7490, "lon": -84.3880}
]

def add_trucks_for_user(username, num_trucks=10):
    with app.app_context():
        # Get the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User {username} not found")
            return False

        # Delete existing trucks for this user
        from models import Truck
        Truck.query.filter_by(user_id=user.id).delete()

        # Create specified number of trucks
        for i in range(num_trucks):
            # Generate random dates within the last year
            last_maintenance = datetime.utcnow() - timedelta(days=random.randint(0, 365))

            # Generate random insurance expiry date
            insurance_days = random.randint(-30, 365)  # Some expired, some active, some expiring soon
            insurance_expiry = datetime.utcnow() + timedelta(days=insurance_days)

            # Pick a random location
            location = random.choice(SAMPLE_LOCATIONS)

            # Slightly randomize the exact position to avoid overlapping markers
            lat_offset = random.uniform(-0.1, 0.1)
            lon_offset = random.uniform(-0.1, 0.1)

            truck = Truck(
                plate_number=f"XP360-{user.id}-{i+1}",
                model=random.choice(TRUCK_MODELS),
                year=random.randint(2018, 2024),
                status=random.choice(TRUCK_STATUSES),
                last_maintenance=last_maintenance,
                destination_city=location["city"],
                destination_state=location["state"],
                destination_set_at=datetime.utcnow(),
                user_id=user.id,
                driver_name=random.choice(DRIVER_NAMES),
                insurance_expiry=insurance_expiry,
                current_latitude=location["lat"] + lat_offset,
                current_longitude=location["lon"] + lon_offset
            )
            db.session.add(truck)

        try:
            db.session.commit()
            print(f"Successfully added {num_trucks} trucks for user {username}")
            return True
        except Exception as e:
            print(f"Error adding trucks: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    # Add trucks for both admin and demo users
    add_trucks_for_user('admin', num_trucks=5)
    add_trucks_for_user('demo', num_trucks=5)