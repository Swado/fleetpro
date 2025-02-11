import random
from app import app, db
from models import User, Truck, Message, Achievement, Reward, DriverAchievement, DriverReward, TripHistory
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
    {"city": "Phoenix", "state": "AZ", "lat": 33.4484, "lon": -112.0740},
    {"city": "San Francisco", "state": "CA", "lat": 37.7749, "lon": -122.4194},
    {"city": "Miami", "state": "FL", "lat": 25.7617, "lon": -80.1918},
    {"city": "Seattle", "state": "WA", "lat": 47.6062, "lon": -122.3321},
    {"city": "Denver", "state": "CO", "lat": 39.7392, "lon": -104.9903},
    {"city": "Atlanta", "state": "GA", "lat": 33.7490, "lon": -84.3880}
]

# Sample message subjects and content for test data
SAMPLE_MESSAGES = [
    {"subject": "Delivery Update", "content": "Running 30 minutes ahead of schedule. Will arrive early."},
    {"subject": "Traffic Alert", "content": "Heavy traffic on I-95. Taking alternate route."},
    {"subject": "Maintenance Required", "content": "Check engine light came on. Requesting maintenance check."},
    {"subject": "Route Change", "content": "Construction ahead. Need to modify route."},
    {"subject": "Weather Warning", "content": "Storm warning issued. Will stop at next safe location."}
]

# Sample achievements data
ACHIEVEMENTS = [
    {
        'name': 'Fuel Efficiency Master',
        'description': 'Achieve 15% better fuel efficiency than fleet average',
        'points': 750,
        'icon': 'fa-gas-pump',
        'category': 'efficiency',
        'criteria': '{"efficiency_improvement": 15}'
    },
    {
        'name': 'Route Optimizer',
        'description': 'Complete 20 trips with optimal route adherence',
        'points': 500,
        'icon': 'fa-route',
        'category': 'efficiency',
        'criteria': '{"optimal_routes": 20}'
    },
    {
        'name': 'Green Fleet Champion',
        'description': 'Maintain idle time below 10% for 30 days',
        'points': 600,
        'icon': 'fa-leaf',
        'category': 'efficiency',
        'criteria': '{"max_idle_percentage": 10, "duration_days": 30}'
    },
    {
        'name': 'Time Management Pro',
        'description': 'Complete 25 deliveries ahead of schedule',
        'points': 450,
        'icon': 'fa-clock',
        'category': 'efficiency',
        'criteria': '{"early_deliveries": 25}'
    },
    {
        'name': 'Distance Warrior',
        'description': 'Drive 10,000 miles with optimal fuel consumption',
        'points': 800,
        'icon': 'fa-road',
        'category': 'efficiency',
        'criteria': '{"miles": 10000, "min_mpg": 7.5}'
    }
]

# Sample rewards data
REWARDS = [
    {
        'name': 'Efficiency Bonus',
        'description': '$200 fuel card reward for exceptional fuel efficiency',
        'points_required': 1000,
        'icon': 'fa-award'
    },
    {
        'name': 'Premium Route Priority',
        'description': 'Priority access to premium routes for 1 month',
        'points_required': 800,
        'icon': 'fa-star'
    },
    {
        'name': 'Performance Recognition',
        'description': 'Featured driver of the month on company dashboard',
        'points_required': 1500,
        'icon': 'fa-trophy'
    },
    {
        'name': 'Vehicle Upgrade',
        'description': 'First choice on next fleet vehicle upgrade',
        'points_required': 2000,
        'icon': 'fa-truck'
    }
]

def add_achievements_and_rewards():
    with app.app_context():
        try:
            # Clear existing achievements and rewards
            DriverAchievement.query.delete()
            DriverReward.query.delete()
            Achievement.query.delete()
            Reward.query.delete()

            # Add achievements
            for achievement_data in ACHIEVEMENTS:
                achievement = Achievement(**achievement_data)
                db.session.add(achievement)

            # Add rewards
            for reward_data in REWARDS:
                reward = Reward(**reward_data)
                db.session.add(reward)

            db.session.commit()
            print("Successfully added achievements and rewards")
        except Exception as e:
            print(f"Error adding achievements and rewards: {e}")
            db.session.rollback()

def add_trucks_for_user(username, num_trucks=10):
    with app.app_context():
        # Get the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User {username} not found")
            return False

        try:
            # First delete related trip histories
            trucks = Truck.query.filter_by(user_id=user.id).all()
            for truck in trucks:
                TripHistory.query.filter_by(truck_id=truck.id).delete()

            # Then delete the trucks
            Truck.query.filter_by(user_id=user.id).delete()
            db.session.commit()

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

                # Set more trucks to active status
                status = random.choices(TRUCK_STATUSES, weights=[0.7, 0.2, 0.1])[0]

                truck = Truck(
                    plate_number=f"XP360-{user.id}-{i+1}",
                    model=random.choice(TRUCK_MODELS),
                    year=random.randint(2018, 2024),
                    status=status,
                    last_maintenance=last_maintenance,
                    destination_city=location["city"],
                    destination_state=location["state"],
                    destination_set_at=datetime.utcnow(),
                    user_id=user.id,
                    driver_name=random.choice(DRIVER_NAMES),
                    driver_phone=f"+1555{random.randint(1000000,9999999)}",
                    insurance_expiry=insurance_expiry,
                    current_latitude=location["lat"] + lat_offset,
                    current_longitude=location["lon"] + lon_offset
                )
                db.session.add(truck)
                db.session.flush()  # Get the truck ID

                # Add some sample messages for this truck
                num_messages = random.randint(1, 3)
                for _ in range(num_messages):
                    message = random.choice(SAMPLE_MESSAGES)
                    msg = Message(
                        sender_id=user.id,
                        receiver_id=user.id,
                        subject=message["subject"],
                        content=message["content"],
                        message_type=random.choice(['normal', 'urgent']),
                        related_truck_id=truck.id,
                        is_read=random.choice([True, False]),
                        timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                    )
                    db.session.add(msg)

            db.session.commit()
            print(f"Successfully added {num_trucks} trucks for user {username}")
            return True
        except Exception as e:
            print(f"Error adding trucks: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    # Add achievements and rewards first
    add_achievements_and_rewards()

    # Then add trucks for both admin and demo users
    add_trucks_for_user('admin', num_trucks=5)
    add_trucks_for_user('demo', num_trucks=5)