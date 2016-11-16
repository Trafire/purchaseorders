import sys, os


INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mail import Mail
from flask_user import login_required , UserManager, UserMixin, SQLAlchemyAdapter
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user


application = Flask(__name__)
application.config.from_pyfile('config.py')
application.config.from_pyfile('instance/config.py')
bcrypt = Bcrypt(application)

############## database setup ###################

#from flaskext.mysql import MySQL

#mysql = MySQL()
#mysql.init_app(application)
#conn = mysql.connect()
#cursor = conn.cursor() 
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(application)
from model import *

db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
user_manager = UserManager(db_adapter, application,register_form=MyRegisterForm)     # Initialize Flask-User


########### Login management############
#from model import User
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view =  "login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()

############## Routes ###################
@application.route('/login',methods=["POST","GET"])
def login():
    form = UsernamePasswordForm(request.form)
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first_or_404()
	if user.is_correct_password(form.password.data):
            login_user(user)
            return redirect(url_for('members'))
        else:

            return redirect(url_for('login'))
    return render_template('login.html', form=form)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@application.route('/')
def index():
    return render_template("index.html")


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegisterForm(request.form)
    form.validate()
    flash_errors(form)
    if form.validate_on_submit(): #request.method == 'POST' and form.validate():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data,password=form.password.data)
 #	return "after user"
        db.session.add(user)
	db.session.commit()

        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
            
@application.route('/members')
@login_required
def members():
    
    return render_template("members.html")


            
