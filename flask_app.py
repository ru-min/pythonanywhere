
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from pytz import timezone
from flask_bmi import calculate

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rumin",
    password="sql12345",
    hostname="rumin.mysql.pythonanywhere-services.com",
    databasename="rumin$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "sfggjkrtygasfbhgj"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone('Asia/Singapore')))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

#comments = []

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    if not current_user.is_authenticated:                                       #check whether user is logged in, before saving his comment in database
        return redirect(url_for('index'))

    comment = Comment(content=request.form["contents"], commenter=current_user)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/bmi_calculator/", methods=["GET", "POST"])
def bmi_calc():
    if request.method == 'POST':
        height = request.form.get("height", type=float)
        weight = request.form.get("weight", type=float)
        if height is None or weight is None:
            error_message = "Please enter both height and weight."
            return render_template("bmi_page.html", error=error_message)
        else:
            bmi = calculate(weight, height)
            if bmi <= 18.5:
                health = "You are underweight! Eat more."
            elif bmi <= 22.9:
                health = "Congrats! You are healthy."
            elif bmi <= 29.9:
                health = "You are overweight. Watch your diet."
            else:
               health = "You are Obese! You need to reduce your weight now! "
            return render_template("bmi_page.html", result=bmi, status=health)
    else:
        return render_template("bmi_page.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))