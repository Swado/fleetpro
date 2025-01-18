from app import app, db
from models import Truck, TripHistory, Invoice
from datetime import datetime, timedelta
import random

# Sample data for random generation
CITIES_BY_STATE = {
    'CA': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
    'TX': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
    'NY': ['New York City', 'Buffalo', 'Albany', 'Rochester'],
    'FL': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
    'IL': ['Chicago', 'Springfield', 'Rockford', 'Peoria']
}

def generate_invoice_number():
    return f"INV-{datetime.utcnow().strftime('%Y%m')}-{random.randint(1000, 9999)}"

def add_sample_trips():
    with app.app_context():
        # Get all trucks
        trucks = Truck.query.all()
        
        for truck in trucks:
            # Generate 3-5 trips per truck
            num_trips = random.randint(3, 5)
            
            for i in range(num_trips):
                # Select random states and cities
                start_state = random.choice(list(CITIES_BY_STATE.keys()))
                end_state = random.choice(list(CITIES_BY_STATE.keys()))
                start_city = random.choice(CITIES_BY_STATE[start_state])
                end_city = random.choice(CITIES_BY_STATE[end_state])
                
                # Generate dates within last 6 months
                days_ago = random.randint(0, 180)
                start_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # 80% chance trip is completed
                is_completed = random.random() < 0.8
                
                trip = TripHistory(
                    truck_id=truck.id,
                    start_city=start_city,
                    start_state=start_state,
                    end_city=end_city,
                    end_state=end_state,
                    start_date=start_date,
                    status='completed' if is_completed else 'in_progress'
                )
                
                if is_completed:
                    # Add end date 1-3 days after start
                    trip.end_date = start_date + timedelta(days=random.randint(1, 3))
                    # Generate reasonable distance based on states
                    trip.distance = random.uniform(300, 1500)
                    
                    # Create invoice for completed trip
                    rate_per_mile = random.uniform(2.5, 3.5)
                    invoice = Invoice(
                        invoice_number=generate_invoice_number(),
                        amount=trip.distance * rate_per_mile,
                        status=random.choice(['paid', 'pending'] * 3 + ['cancelled']),  # 3:3:1 ratio
                        created_at=trip.end_date
                    )
                    trip.invoice = invoice
                
                db.session.add(trip)
        
        try:
            db.session.commit()
            print("Successfully added sample trips and invoices")
        except Exception as e:
            print(f"Error adding sample data: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_sample_trips()
