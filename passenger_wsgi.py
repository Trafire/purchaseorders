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
from views import *


            
