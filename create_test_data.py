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

def create_test_data():
    with app.app_context():
        # Create 5 test users
        for i in range(1, 6):
            username = f"fleet_manager_{i}"
            # Check if user already exists
            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    email=f"fleet{i}@example.com"
                )
                user.set_password(f"password{i}")
                db.session.add(user)
                db.session.commit()
                
                # Create random number of trucks (2-8) for each user
                num_trucks = random.randint(2, 8)
                for j in range(num_trucks):
                    # Generate random dates within the last year
                    last_maintenance = datetime.utcnow() - timedelta(days=random.randint(0, 365))
                    
                    truck = Truck(
                        plate_number=f"TRK-{i}{j}",
                        model=random.choice(TRUCK_MODELS),
                        year=random.randint(2018, 2024),
                        status=random.choice(TRUCK_STATUSES),
                        last_maintenance=last_maintenance,
                        user_id=user.id
                    )
                    db.session.add(truck)
                db.session.commit()
                print(f"Created user {username} with {num_trucks} trucks")

if __name__ == '__main__':
    create_test_data()
