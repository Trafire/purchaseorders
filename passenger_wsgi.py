import sys, os


INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, render_template, request
from flask_mail import Mail
from flask_user import login_required , UserManager, UserMixin, SQLAlchemyAdapter

application = Flask(__name__)
application.config.from_pyfile('config.py')
application.config.from_pyfile('instance/config.py')

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
'''
@application.route('/register', methods=["POST","GET"])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        psw = request.form['psw'].strip()
        if email[-15:] != "@fleurametz.com":
            error = "Must Register with FleuraMetz Email"
        if name == '' or email == '' or psw == '':
            error = "Must fill in all fields"
        if error:    
            return render_template("failure.html", error=error)
        return render_template("register.html",name=name,email=email,psw=psw)
        
    else:
        return render_template("registration.html")
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
            

@application.route('/members')
#@login_required
def members_page():
    return render_template_string("members.html")

            
