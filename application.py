import os
import WTF_classes

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

os.environ["DATABASE_URL"] = "postgres://rstrmsgknaerel:b27002260a792f02d00ba9d23da8e41d1d7a375ea03aa44210fcf8fe4b082a86@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dfofnj4eu4rg1q"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: hello"


@app.route("/register", methods = ["POST"])
def register():
	form = Registration(request.form)

