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
def login():
    return render_template("login.html")

@application.route('/')
def index():
    return render_template("index.html")

'''
@application.route('/registration')
def registration():
    return render_template("registration.html")
'''

@application.route('/register', methods=["POST","GET"])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        psw = request.form['psw'].strip()
        if email[-15:] == "@fleurametz.com":
            error = "Must Register with FleuraMetz Email"
            return render_template("failure.html",error=error)
            
        
        return render_template("register.html",name=name,email=email,psw=psw)
    else:
        return render_template("registration.html")
