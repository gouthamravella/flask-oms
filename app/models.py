import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class Location(db.Model):
    """
    create a Location table
    """

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(60), unique=True)

    menuitems = db.relationship("MenuItems",backref = 'locations',
                                 lazy = 'dynamic')
    
    stall_list = db.relationship("Stalls", backref = 'locations', 
                                lazy = 'dynamic')

    def __repr__(self):
        return '<Location: {}>'.format(self.location)

class MenuItems(db.Model):
    """
    create a MenuItems table
    """

    __tablename__ = 'menuitems'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))
    stall_id = db.Column(db.Integer, db.ForeignKey('stalls.id'))
    location_id =  db.Column(db.Integer, db.ForeignKey('locations.id'))

    def __repr__(self):
        return '<MenuItems: {}>'.format(self.name)

class Stalls(db.Model):
    """
    create a Stalls table
    """

    __tablename__ = 'stalls'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(255))
    ownername = db.Column(db.String(60))
    contact_number = db.Column(db.String(25))
    mobile_number = db.Column(db.String(25))
    address = db.Column(db.String(425))
    notes = db.Column(db.String(255))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    menuitems = db.relationship('MenuItems', backref = 'menu_list',
                                 lazy = 'dynamic')

    def __repr__(self):
        return '<Stalls: {}'.format(self.name)

class Orders(db.Model):
    """
    create a Orders table
    """

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    tablenumber = db.Column(db.Integer)
    notes = db.Column(db.String(255))
    orderstatus = db.Column(db.Integer, db.ForeignKey('status.id'))
    email_sent = db.Column(db.String(10)) #sent an email when the flag is set to 'S'
    sms_sent = db.Column(db.String(10)) #sent an sms when the flag is set to 'S'
    processed = db.Column(db.String(10)) #flag 'N' or 'Y'
    datecreated = db.Column(db.TIMESTAMP)
    dateupdated = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    orders_list = db.relationship('OrdersList', backref = 'order_items', lazy = 'dynamic')

    def __repr__(self):
        return '<Orders: {}'.format(self.tablenumber)

class OrdersList(db.Model):
    """
    create a OrdersList table
    """

    __tablename__ = 'orderslist'

    id = db.Column(db.Integer, primary_key = True)
    menuitems_id = db.Column(db.Integer, db.ForeignKey('menuitems.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    stall_id = db.Column(db.Integer, db.ForeignKey('stalls.id'))
    orderitem_confirmation = db.Column(db.String(10))
    approximate_time_in_minutes = db.Column(db.Integer)
    time_confirmation = db.Column(db.String(10))
    processed = db.Column(db.String(10))
    datecreated = db.Column(db.TIMESTAMP)
    dateupdated = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '<OrderList: {}'.format(self.order_id)

class Customers(db.Model):
    """
    create a Customers table
    """

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60))
    mobile_number = db.Column(db.String(25))
    email_id = db.Column(db.String(55))
    datecreated = db.Column(db.TIMESTAMP)
    dateupdated = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '<Customer: {}'.format(self.name)

class Status(db.Model):
    """
    create a Status table
    """

    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), unique = True)
    datecreated = db.Column(db.TIMESTAMP)
    dateupdated = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return '<Status: {}'.format(self.name)
