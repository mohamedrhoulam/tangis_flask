from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tangis.db'
app.config['SECRET_KEY'] = 'your_secret_key'


admin = Admin(app, template_mode='bootstrap3')

db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    CIN = db.Column(db.String(50), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    CIN = db.Column(db.String(50), nullable=False, unique=True)
    CNSS = db.Column(db.String(50), nullable=False, unique=True)
    salary = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('bookings', lazy=True))

class ClientModelView(ModelView):
    column_searchable_list = ['first_name', 'last_name']

class BookingModelView(ModelView):
    column_searchable_list = ['date', 'client_id']

class CourseModelView(ModelView):
    column_searchable_list = ['location', 'course_type', 'course']

class EmployeeModelView(ModelView):
    column_searchable_list = ['first_name', 'last_name', 'CIN', 'CNSS']


def create_tables():
    with app.app_context():
        db.create_all()


# startic from endpoint '/' serve static files from the folder 'static'
@app.route('/')
def index():
    # server static file 'index.html' from folder 'static'
    return app.send_static_file('index.html')

@app.route('/book', methods=['POST'])
def create_booking():
    # get the request object
    req = request.form
    print(req)
    # get the request body
    # Get the client_id, date, and time from the request body
    client_id = req.get('client_id')

    # fetch the client from the database
    try:
        client = Client.get(client_id)
    except Exception as e:
        return redirect(url_for('booking_error'))

    date = datetime.strptime(req.get('date'), '%Y-%m-%d').date()
    time = datetime.strptime(req.get('time'), '%H:%M').time()

    # Add an entry to the database's BOOKINGS table
    new_booking = Booking(client=client, date=date, time=time)
    db.session.add(new_booking)

    try:
        db.session.commit()

        # If the entry is added successfully, return a response with status code 200 then redirect to '/success'
        return redirect(url_for('booking_success'))

    except Exception as e:
        db.session.rollback()

        # If an error occurs, redirect to '/error'
        return redirect(url_for('booking_error'))
    
@app.route('/booking_success')
def booking_success():
    return app.send_static_file('booking_success.html')

@app.route('/booking_error')
def booking_error():
    return app.send_static_file('booking_failure.html')




# admin.add_view(ModelView(Client, db.session))
# admin.add_view(ModelView(Course, db.session))
# admin.add_view(ModelView(Employee, db.session))
# admin.add_view(ModelView(Booking, db.session))
admin.add_view(ClientModelView(Client, db.session))
admin.add_view(CourseModelView(Course, db.session))
admin.add_view(EmployeeModelView(Employee, db.session))
admin.add_view(BookingModelView(Booking, db.session))



if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='10.126.219.71')
