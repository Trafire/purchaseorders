import sys, os
INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())


from flask import Flask, render_template, request
application = Flask(__name__)
application.config.from_object('config')
application.config.from_pyfile('config.py')

@application.route('/login')
@application.route('/')
def index():
    return render_template("login.html")


@application.route('/registration')
def registration():
    return render_template("registration.html")

@application.route('/register', methods=["POST"])
def register():
    name = request.form['name']
    return render_template("register.html",name=name)
