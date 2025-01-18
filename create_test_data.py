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

            truck = Truck(
                plate_number=f"XP360-{user.id}-{i+1}",
                model=random.choice(TRUCK_MODELS),
                year=random.randint(2018, 2024),
                status=random.choice(TRUCK_STATUSES),
                last_maintenance=last_maintenance,
                user_id=user.id
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