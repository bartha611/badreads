import os
import sys
from WTF_classes import Registration, Login, SearchForm

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, session, render_template, request, flash, redirect,  url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'This_is_a_secret_key'
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods = ["GET", "POST"])
def register():
	form = Registration()
	if request.method == "POST" and form.validate_on_submit():
		username = request.form["username"]
		password = request.form["password"]
		email = request.form["email"]
		hashed_password = generate_password_hash(password)
		check_email_exists = db.execute("SELECT email FROM person WHERE email = :email", 
			{"email": email}).fetchall()
		check_username_exists = db.execute("SELECT username FROM person WHERE username = :username",
			{"username":username})
		if len(check_user_exists) != 0 and len(check_username_exists) != 0:
			flash(u'Email and/or username already exists!', 'error')
			return redirect(url_for('register'))
		db.execute("INSERT INTO person(username, password, email) VALUES (:username, :password, :email)", 
			{"username": username, "password": hashed_password, "email": email})
		db.commit()
		flash('You have successfully registered')
		return redirect(url_for('index'))
	return render_template('register.html', form = form)


@app.route("/login", methods = ["GET","POST"])
def login():
	form = Login()
	if request.method == "POST" and form.validate_on_submit():
		if 'username' in session:
			flash('You are already logged in')
			return redirect(url_for('index'))
		email = request.form["email"]
		password = request.form["password"]
		hashed_password = generate_password_hash(password)
		person = db.execute("SELECT username, email, password FROM person WHERE email = :email", 
			{"email": email}).fetchall()
		if len(person) == 0:
			flash('Email does not exist in database')
			return redirect(url_for('login'))
		else:
			for person in person:
				db_password = person.password
				db_email = person.email
				db_username = person.username
			if email == db_email and check_password_hash(db_password, form.password.data):
				session['username'] = db_username
				flash('login successful!!')
				return redirect(url_for('index'))
			elif check_password_hash(password, db_password) == False:
				flash('password has failed')
				return redirect(url_for('login'))
	return render_template('login.html', form = form)

@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))
	
@app.route('/search', methods = ["GET", "POST"])
def search():
	form = SearchForm()
	if request.method == "POST" and form.validate_on_submit():
		query = request.form["search"]
		return redirect(url_for('search_results',query=query))
	return render_template('search.html', form=form)

@app.route('/search_results', methods=["GET", "POST"])
def search_results():
	query = request.args.get('query')
	try:
		query = int(query)
		results = db.execute("SELECT isbn,title,author FROM books WHERE isbn LIKE '%:isbn%'", 
			{"isbn":query}).fetchall()
	except ValueError:
		query = '%' + query + '%'
		results = db.execute("""SELECT isbn,title,author,year FROM books
		 WHERE UPPER(author) LIKE UPPER(:query) or
		 UPPER(TITLE) LIKE UPPER(:query)""", {"query":query}).fetchall()
	return render_template('search_results.html', messages=results)

@app.route('/book/<title>', methods = ["GET", "POST"])
def book(title):
	book_result = db.execute("SELECT * FROM books WHERE title = :title",
		{"title": title}).fetchall()
	bookId = book_result[0][0]
	book_reviews = db.execute("SELECT * FROM reviews WHERE bookid = :bookid", 
		{"bookid":bookId}).fetchall()
	username = session['username']
	user_review = db.execute("SELECT * FROM reviews WHERE username = :username",
		{"username":username}).fetchall()
	return render_template('book.html', book = book_result, reviews = book_reviews, user_review = user_review)


	

if __name__ == '__main__':
	app.run(debug=True)


