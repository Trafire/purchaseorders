import sys, os
INTERP = os.path.join(os.environ['HOME'], 'purchaseorders.fleurametztoronto.com', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())


from flask import Flask, render_template
application = Flask(__name__)


@application.route('/')
def index():
    return render_template("login.html")

