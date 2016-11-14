from passenger_wsgi import db
from flask_user import UserMixin
from flask_user.forms import RegisterForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
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

    def is_active(self):
      return self.is_enabled

# Define the Role DataModel
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))    

class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[validators.Required('First name is required')])
    last_name  = StringField('Last name',  validators=[validators.Required('Last name is required')])
    password  = PasswordField('Password',  validators=[validators.Required('Password is required')])
    email = StringField('Email', validators=[validators.Required('An FM Email is required')]) 
	


