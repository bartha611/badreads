import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

os.environ["DATABASE_URL"] = "database_url"
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
	username = StringField('username', validators=[InputRequired(), Length(min=10, max=70), Email("must provide a valid email between 10 to 50 characters")], description = "email")
	password = PasswordField('Password', validators=[InputRequired(), 
		EqualTo('confirm', message = "Passwords must match")])
	confirm = PasswordField('Confirm Password')
	submit = SubmitField('Submit')



@app.route("/")
def index():
    return render_template('login.html')


@app.route("/register", methods = ["GET", "POST"])
def register():
	form = Registration(request.form)
	if request.method == "POST" and form.validate_on_submit():
		username = request.form["username"]
		password = request.form["password"]
		hashed_password = generate_password_hash(password)
		db.execute("INSERT INTO person(username, password) VALUES (:username, :password)", {"username": username, "password": hashed_password})
		db.commit()
		return "You registered successfully!!!"
	return render_template('register.html', form = form)


if __name__ == '__main__':
	app.run(debug=True)


