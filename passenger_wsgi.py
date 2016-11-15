import sys, os


INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, render_template, request,redirect, url_for, flash
from flask_mail import Mail
from flask_user import login_required , UserManager, UserMixin, SQLAlchemyAdapter
from flask_bcrypt import Bcrypt

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

############## Routes ###################
@application.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST': 
        return render_template("index.html")
    else:
        return render_template("login.html")

@application.route('/')
def index():
    return render_template("index.html")


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = MyRegisterForm(request.form)
    if request.method == 'POST':# and form.validate():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data,password=form.password.data)
#	return "after user"
        db.session.add(user)
	db.session.commit()

        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
            
@application.route('/members')
#@login_required
def members_page():
    return render_template_string("members.html")


            
