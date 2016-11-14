
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

@application.route('/members')
#@login_required
def members_page():
    return render_template_string("members.html")
