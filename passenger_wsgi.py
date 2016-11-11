import sys, os


INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, render_template, request



app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')


######## Routes #############

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == 'POST': 
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST","GET"])
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

@app.route('/members')
@login_required
def members_page():
    return render_template_string("members.html")

            
