from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey(
        'reservation.reservation_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    # Add additional payment-related fields as needed


class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey(
        'car_list.car_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    pickup_location = db.Column(db.String(100), nullable=False)
    return_location = db.Column(db.String(100), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    insurance_option = db.Column(db.String(50))
    is_completed = db.Column(db.Boolean, default=False)
    additional_notes = db.Column(db.Text)
    discount = db.Column(db.Float, default=0)

    # Define the relationships
    car = db.relationship('CarList', backref='reservations')
    user = db.relationship('User', backref='reservations')

class CarList(db.Model):
    __tablename__ = 'car_list'

    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer)
    color = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    fuel_type = db.Column(db.String(20))
    engine_capacity = db.Column(db.Float)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100))
    license_plate = db.Column(db.String(20))
    vehicle_identification_number = db.Column(db.String(50))
    seating_capacity = db.Column(db.Integer)
    body_type = db.Column(db.String(50))
    drive_type = db.Column(db.String(50))
    fuel_consumption = db.Column(db.Float)
    features = db.Column(db.Text)
    insurance_information = db.Column(db.Text)
    maintenance_records = db.Column(db.Text)
