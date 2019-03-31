import os
import sys
from WTF_classes import Registration, Login
import urllib.request

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, session, render_template, request, flash, redirect,  url_for,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['UPLOAD_FOLDER'] = os.path.join('/static', 'img')

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


# User registration for website
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
			{"username":username}).fetchall()
		if len(check_username_exists) != 0 and len(check_username_exists) != 0:
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

@app.route('/search_results', methods=["GET", "POST"])
def search_results():
	query = request.args.get("query")
	print(query)
	try:
		query = int(query)
		results = db.execute("SELECT * FROM books WHERE isbn LIKE '%:isbn%'", 
			{"isbn":query}).fetchall()
	except ValueError:
		query = '%' + query + '%'
		results = db.execute("""SELECT * FROM books
		 WHERE UPPER(author) LIKE UPPER(:query) or
		 UPPER(TITLE) LIKE UPPER(:query)""", {"query":query}).fetchall()
	return render_template('search_results.html', messages=results)

@app.route('/book/<isbn>', methods = ["POST", "GET"])
def book(isbn):
	print(session['username'])
	book_result = db.execute("SELECT * FROM books WHERE isbn = :isbn",
		{"isbn": isbn}).fetchall()
	average_rating = book_result[0].average_score
	width_star = round(average_rating / 5,2)*100
	bookId = book_result[0].bookid
	book_reviews = db.execute("""
		SELECT review_rating,review_text,username 
		FROM reviews r
		INNER JOIN person p ON (r.personId = p.personId)
		WHERE bookid = :bookid""", 
		{"bookid":bookId}).fetchall()
	username = session['username']
	user_review = db.execute("""
		SELECT * FROM reviews
		JOIN person ON (person.personid = reviews.personid)
		WHERE username = :username AND bookid = :bookid
		""", {"username":username, "bookid":bookId}).fetchall()
	return render_template('book.html', book = book_result, reviews = book_reviews, user_review = user_review,width_star = width_star)
	# except:
	#  	flash('User not logged in')
	#  	return redirect(url_for('index'))

@app.route('/review/<isbn>', methods = ["GET","POST"])
def review(isbn):
	review_book = db.execute("""
		SELECT *
		FROM books
		WHERE isbn = :isbn""", {"isbn":isbn}).fetchall()
	return render_template('review_edit.html', book = review_book)

#add review to database
@app.route('/add_rating', methods = ["POST"])
def add_rating():
	isbn = request.json['isbn']
	stars = request.json['stars']
	username = session['username']
	current_rating = request.json['current_rating']
	userid = db.execute("""
		SELECT personid
		FROM person 
		WHERE username = :username""",
		{"username":username}).first()
	bookid = db.execute("""
		SELECT bookid
		FROM books
		WHERE isbn = :isbn""",
		{"isbn":isbn}).first()
	if current_rating == None:
		db.execute("INSERT INTO reviews(review_rating, personid, bookid) VALUES (:rating, :personid, :bookid)", 
		{"rating":stars, "personid":userid[0], "bookid":bookid[0]})
		db.commit()
		#update book's average review rating and total reviews
		db.execute("""
			UPDATE books
				SET average_score = 
				(SELECT AVG(r.review_rating)
				FROM reviews r
				INNER JOIN books b ON (r.bookId = b.bookId)
				WHERE b.isbn = :isbn),
				review_count = 
				(SELECT COUNT(r.review_rating)
				FROM reviews r
				INNER JOIN books b ON (b.bookId = r.bookId)
				WHERE b.isbn = :isbn)
			WHERE books.isbn = :isbn
			""", {"isbn": isbn})
		db.commit()
	else:
		db.execute("""
			UPDATE reviews
				SET review_rating = :stars
			WHERE reviews.personId = :userid AND reviews.bookId = :bookid
			""",{"stars":stars,"userid":userid[0],"bookid":bookid[0]})
		db.commit()
		db.execute("""
			UPDATE books
				SET average_score = 
				(SELECT AVG(r.review_rating)
				FROM reviews r
				INNER JOIN books b ON (r.bookId = b.bookId)
				WHERE b.isbn = :isbn)
			WHERE books.isbn = :isbn
			""", {"isbn": isbn})
		db.commit()
	return jsonify({'isbn':isbn, 'stars': stars})

@app.route('/get_user_rating', methods = ["GET"])
def get_user_rating():
	isbn = request.args.get('isbn')
	username = session['username']
	user_rating = db.execute("""
		SELECT r.review_rating
		FROM reviews AS r
		INNER JOIN person ON (r.personid = person.personid)
		INNER JOIN books ON (r.bookid = books.bookid)
		WHERE isbn = :isbn AND username = :username""",
		{"isbn": isbn, "username": username}).fetchall()
	if len(user_rating) == 0:
		return jsonify({'user_rating': None})
	return jsonify({'user_rating': user_rating[0].review_rating})
	

@app.route('/add_review', methods = ["POST"])
def add_review():
	review_bookid = request.args.get('book_id')
	review_text = request.form['review']
	username = session['username']
	userid = db.execute("""
		SELECT personid
		FROM person 
		WHERE username = :username""",
		{"username":username}).first()
	db.execute("""
		UPDATE reviews r
			SET review_text = :review
		WHERE r.personid = :userid AND r.bookId = :bookId""", {"userid":userid[0], "review":review_text,"bookId": review_bookid})
	db.commit()
	#reroute back to book page
	isbn = db.execute("""
		SELECT isbn
		FROM books b
		WHERE b.bookId = :bookid""",
		{"bookid":review_bookid}).first()
	return redirect(url_for('book', isbn = isbn[0]))

@app.route('/api/<isbn>', methods = ["GET"])
def api(isbn):
	data = db.execute("""
		SELECT *
		FROM books
		WHERE isbn = :isbn""",{"isbn":isbn}).fetchall()
	d = [dict(row) for row in data]
	return jsonify(d[0])

if __name__ == '__main__':
	app.run(debug=True)