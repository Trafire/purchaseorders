import sys, os


INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, render_template, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

application = Flask(__name__)
application.config.from_object('config')
application.config.from_pyfile('config.py')




########User Setup#############

class User(db.Model, UserMixin):
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

    def is_active(self):
      return self.is_enabled

# Create all database tables
db.create_all()

# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, app)     # Initialize Flask-User 

######## Routes #############

@application.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST': 
        return render_template("index.html")
    else:
        return render_template("login.html")

@application.route('/')
def index():
    return render_template("index.html")

@application.route('/register', methods=["POST","GET"])
def register():
    error = None
    if request.method == 'POST':
        first_name = request.form['firstname'].strip()
        last_name = request.form['lastname'].strip()        
        email = request.form['email'].strip()
        psw = request.form['psw'].strip()
        if email[-15:] != "@fleurametz.com":
            error = "Must Register with FleuraMetz Email"
        if name == '' or email == '' or psw == '':
            error = "Must fill in all fields"
        if error:    
            return render_template("failure.html", error=error)
        return render_template("register.html",firstname=firstname,lastname=lastname,email=email,psw=psw)
    else:
        return render_template("registration.html")

@application.route('/members')
@login_required
def members_page():
    return render_template_string("members.html")

            
