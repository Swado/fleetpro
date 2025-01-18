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

def generate_invoice_number(date):
    return f"INV-{date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

def add_sample_trips():
    with app.app_context():
        try:
            # Clear existing trip history and invoices
            Invoice.query.delete()
            TripHistory.query.delete()
            db.session.commit()
            print("Cleared existing trips and invoices")

            # Get all trucks
            trucks = Truck.query.all()

            for truck in trucks:
                # Generate trips for the last 90 days
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=90)
                current_date = start_date

                while current_date <= end_date:
                    # 80% chance of having a trip on any given day
                    if random.random() < 0.8:
                        # Select random states and cities
                        start_state = random.choice(list(CITIES_BY_STATE.keys()))
                        end_state = random.choice(list(CITIES_BY_STATE.keys()))
                        start_city = random.choice(CITIES_BY_STATE[start_state])
                        end_city = random.choice(CITIES_BY_STATE[end_state])

                        # Generate random runtime and idle time
                        runtime = random.uniform(6, 10)  # 6-10 hours of runtime
                        idle_time = random.uniform(1, 3)  # 1-3 hours of idle time

                        trip = TripHistory(
                            truck_id=truck.id,
                            start_city=start_city,
                            start_state=start_state,
                            end_city=end_city,
                            end_state=end_state,
                            start_date=current_date,
                            end_date=current_date + timedelta(days=1),
                            status='completed',
                            runtime_hours=runtime,
                            idle_time_hours=idle_time,
                            distance=random.uniform(300, 1500)
                        )

                        # Create invoice for the trip
                        rate_per_mile = random.uniform(2.5, 3.5)
                        invoice = Invoice(
                            invoice_number=generate_invoice_number(current_date),
                            amount=trip.distance * rate_per_mile,
                            status=random.choice(['paid', 'pending'] * 3 + ['cancelled']),  # 3:3:1 ratio
                            created_at=trip.end_date
                        )
                        trip.invoice = invoice
                        db.session.add(trip)

                    current_date += timedelta(days=1)

            db.session.commit()
            print("Successfully added sample trips and invoices")

        except Exception as e:
            print(f"Error adding sample data: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_sample_trips()