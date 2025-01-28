from app import app, db
from models import User, Truck
import random
from datetime import datetime, timedelta

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
    {"city": "Phoenix", "state": "AZ", "lat": 33.4484, "lon": -112.0740}
]

def add_trucks_for_user(username, num_trucks=10):
    with app.app_context():
        # Get the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User {username} not found")
            return False

        # Delete existing trucks for this user
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
                current_latitude=location["lat"],
                current_longitude=location["lon"]
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
    # Add trucks for admin user
    add_trucks_for_user('admin')