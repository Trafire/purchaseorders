from passenger_wsgi import db, bcrypt
from flask_user import UserMixin
from flask_user.forms import RegisterForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators,TextField
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(64), nullable=False)
    reset_password_token = db.Column(db.String(100), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    
    purchaseorders = db.relationship('PurchaseOrders', 
            backref=db.backref('users', lazy='dynamic'))

    
    def is_active(self):
      return self.is_enabled

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        if bcrypt.check_password_hash(self._password, plaintext):
            return True

        return False

class Suppliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(50), nullable=False, unique=True)
    purchaseorders = db.relationship('PurchaseOrders', 
            backref=db.backref('suppliers', lazy='dynamic')

class PurchaseOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    authorizing_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    invoice_date = db.Column(db.DateTime)
    suppliers_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    client = db.Column(db.String(255))
    status = db.Column(db.Integer)

    purchases = db.relationship('Purchases', 
            backref=db.backref('purchaseorders', lazy='dynamic')
    
     

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_orders = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    Items_id = db.Column(db.Integer, db.ForeignKey('items.id'))

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True)
    items = db.relationship('Items', 
            backref=db.backref('Categories', lazy='dynamic')

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), unique=True)
    items = db.relationship('Items', 
            backref=db.backref('Products', lazy='dynamic')
    
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Products_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    Categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))  
    grade = db.Column(db.String(25))
    purchases = db.relationship('Purchases', 
            backref=db.backref('Items', lazy='dynamic')
    
    
                     


# Define the Role DataModel
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))    


class MyRegisterForm(RegisterForm):
    first_name = StringField('First Name', validators=[validators.Required('First name is required')])
    last_name  = StringField('Last Name', validators=[validators.Required('Last name is required')])
    password  = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    email = StringField('Email', validators=[validators.Email('An FM Email is required')]) 
    confirm = PasswordField('Confirm Password')	


class UsernamePasswordForm(Form):
    username = StringField('Username', validators=[validators.Required("Must Provide Username")])
    password = PasswordField('Password', validators=[validators.Required("Must Enter a password")])
    
