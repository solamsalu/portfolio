from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12192129s@localhost/selamdb'
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your secret key

db = SQLAlchemy(app)

class CarList(db.Model):
    __tablename__ = 'CarList'
    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    
class Customer(db.Model):
    __tablename__ = 'Customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)


class Reservation(db.Model):
    __tablename__ = 'Reservation'
    reservation_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'Customer.customer_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    customer = db.relationship('Customer', backref='reservations')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all_cars')
def all_cars():
    return render_template('carListing.html')

@app.route('/select_car/<int:car_id>')
def select_car(car_id):
    # Query the database for a car with the given car_id
    car = CarList.query.get(car_id)
    if car is None:
        # If no car with this ID exists, return a 404 error.
        abort(404)
    # ... code to handle car selection ...
    return redirect(url_for('reserve', car_id=car.car_id))


@app.route('/reservation', methods=['GET', 'POST'])
@app.route('/reservation/<int:car_id>', methods=['GET', 'POST'])
def reserve(car_id=None):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        car_id = int(request.form.get('car_id'))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        customer = Customer(name=name, email=email,
                            phone=phone, address=address)
        db.session.add(customer)

        try:
            db.session.commit()
            flash('Customer created successfully')

            reservation = Reservation(customer_id=customer.customer_id,
                                      car_id=car_id,
                                      start_date=start_date,
                                      end_date=end_date)
            db.session.add(reservation)
            db.session.commit()

            flash('Reservation created successfully')

        except SQLAlchemyError as e:
            flash('An error occurred while creating the reservation: ' + str(e))
            db.session.rollback()

        finally:
            # Close the session
            db.session.close()

        return redirect('/')

    return render_template('reservation_form.html', car_id=car_id)


@app.route('/suvs')
def suvs():
    return render_template('suvs.html')


@app.route('/sedans')
def sedans():
    return render_template('sedans.html')


@app.route('/vans')
def vans():
    return render_template('vans.html')


@app.route('/luxury')
def luxury():
    return render_template('luxury.html')


@app.route('/addis')
def addis():
    return render_template('location_addis.html')


@app.route('/dire')
def dire():
    return render_template('location_dire.html')


@app.route('/hawassa')
def hawassa():
    return render_template('location_hawassa.html')


@app.route('/gondar')
def gondar():
    return render_template('location_gondar.html')


@app.route('/mekelle')
def mekelle():
    return render_template('location_mekelle.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/admin')
# def admin():
#     return render_template('admin_login.html')


# @app.route('/reservation', methods=['GET', 'POST'])
# def reservation():
#     if request.method == 'POST':
#         # Retrieve form data
#         customer_id = request.form['customer_id']
#         car_id = request.form['car_id']
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']

#         # Create a new Reservation object
#         reservation = Reservation(
#             customer_id=customer_id, car_id=car_id, start_date=start_date, end_date=end_date)

#         # Add the reservation to the database
#         db.session.add(reservation)
#         db.session.commit()

#         return 'Reservation created successfully'

#     return render_template('reservation_form.html')


# @app.route('/customers')
# def customers():
#     customers = Customer.query.all()
#     return render_template('customers.html', customers=customers)


# @app.route('/customers/add', methods=['GET', 'POST'])
# def add_customer():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         address = request.form['address']

#         customer = Customer(name=name, email=email,
#                             phone=phone, address=address)
#         db.session.add(customer)
#         db.session.commit()

#         return redirect('/customers')

#     return render_template('add_customer.html')


# @app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
# def edit_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)

#     if request.method == 'POST':
#         customer.name = request.form['name']
#         customer.email = request.form['email']
#         customer.phone = request.form['phone']
#         customer.address = request.form['address']

#         db.session.commit()
#         return redirect('/customers')

#     return render_template('edit_customer.html', customer=customer)


# @app.route('/customers/delete/<int:customer_id>', methods=['POST'])
# def delete_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     db.session.delete(customer)
#     db.session.commit()
#     return redirect('/customers')


# @app.route('/cars')
# def cars():
#     cars = CarList.query.all()
#     return render_template('car.html', cars=cars)


# @app.route('/cars/add', methods=['GET', 'POST'])
# def add_car():
#     if request.method == 'POST':
#         make = request.form['make']
#         model = request.form['model']
#         year = request.form['year']
#         daily_rate = request.form['daily_rate']
#         # mileage = request.form['mileage']
#         # color = request.form['color']
#         # Retrieve other car-related fields

#         car = CarList(make=make, model=model, year=year,
#                       daily_rate=daily_rate)
#         # Set other car-related fields

#         db.session.add(car)
#         db.session.commit()

#         return redirect('/cars')

#     return render_template('add_car.html')


# @app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
# def edit_car(car_id):
#     car = CarList.query.get_or_404(car_id)

#     if request.method == 'POST':
#         car.make = request.form['make']
#         car.model = request.form['model']
#         car.year = request.form['year']
#         car.daily_rate = request.form['daily_rate']
#         # car.mileage = request.form['mileage']
#         # car.color = request.form['color']
#         # Update other car-related fields

#         db.session.commit()
#         return redirect('/cars')

#     return render_template('edit_car.html', car=car)


# @app.route('/cars/delete/<int:car_id>', methods=['POST'])
# def delete_car(car_id):
#     car = CarList.query.get_or_404(car_id)
#     db.session.delete(car)
#     db.session.commit()
#     return redirect('/cars')


# @app.route('/payments/add', methods=['GET', 'POST'])
# def add_payment():
#     if request.method == 'POST':
#         reservation_id = request.form['reservation_id']
#         amount = request.form['amount']
#         payment_date = request.form['payment_date']
#         payment_method = request.form['payment_method']
#         transaction_id = request.form['transaction_id']
#         status = request.form['status']
#         # Retrieve other payment-related fields

#         payment = Payment(reservation_id=reservation_id, amount=amount, payment_date=payment_date,
#                           payment_method=payment_method, transaction_id=transaction_id, status=status)
#         # Set other payment-related fields

#         db.session.add(payment)
#         db.session.commit()

#         return redirect('/payments')

#     return render_template('add_payment.html')


# @app.route('/payments/edit/<int:payment_id>', methods=['GET', 'POST'])
# def edit_payment(payment_id):
#     payment = Payment.query.get_or_404(payment_id)

#     if request.method == 'POST':
#         payment.reservation_id = request.form['reservation_id']
#         payment.amount = request.form['amount']
#         payment.payment_date = request.form['payment_date']
#         payment.payment_method = request.form['payment_method']
#         payment.transaction_id = request.form['transaction_id']
#         payment.status = request.form['status']
#         # Update other payment-related fields

#         db.session.commit()
#         return redirect('/payments')

#     return render_template('edit_payment.html', payment=payment)


# @app.route('/reservations/create', methods=['GET', 'POST'])
# def create_reservation():
#     def calculate_total_cost(car, start_date, end_date, discount=0):
#         # Perform calculations to determine the total cost
#         # Consider factors like car rental rate, duration, additional fees, and discounts

#         # Assuming you have a daily_rate property in the CarList model
#         daily_rate = car.daily_rate
#         duration = (end_date - start_date).days
#         base_cost = daily_rate * duration

#         total_cost = base_cost - (base_cost * discount)

#         return total_cost
#     if request.method == 'POST':
#         car_id = request.form['car_id']
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']
#         pickup_location = request.form['pickup_location']
#         return_location = request.form['return_location']
#         insurance_option = request.form['insurance_option']
#         additional_notes = request.form['additional_notes']
#         discount = calculate_discount()

#         # Calculate total cost based on selected car and dates
#         car = CarList.query.get(car_id)
#         total_cost = calculate_total_cost(car, start_date, end_date, discount)

#         # Create the reservation object
#         reservation = Reservation(
#             car_id=car_id,
#             customer_id=current_user.customer_id,  # Assuming you have a current user object
#             start_date=start_date,
#             end_date=end_date,
#             pickup_location=pickup_location,
#             return_location=return_location,
#             total_cost=total_cost,
#             insurance_option=insurance_option,
#             additional_notes=additional_notes,
#             discount=discount

#         )

#         db.session.add(reservation)
#         db.session.commit()

#         return redirect(url_for('reservation_success'))

#     # Retrieve available cars for the dropdown
#     available_cars = CarList.query.filter_by(is_available=True).all()

#     return render_template('create_reservation.html', available_cars=available_cars)

#    if __name__ == '__main__':
 #       app.run()
