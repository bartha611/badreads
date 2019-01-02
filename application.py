import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

app = Flask(__name__)

os.environ["DATABASE_URL"] = "postgres://rstrmsgknaerel:b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dfofnj4eu4rg1q"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'THIS_IS_A_SECRET_KEY'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class Registration(FlaskForm):
	username = StringField('username required', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired(), 
		EqualTo('confirm', message = "Passwords must match")])
	confirm = PasswordField('Confirm Password')


@app.route("/")
def index():
    return render_template('login.html')


@app.route("/register", methods = ["GET", "POST"])
def register():
	form = Registration()
	return render_template('register.html', form = form)


