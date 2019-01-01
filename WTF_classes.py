from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class Registration(FlaskForm):
	username = StringField('username required', validators=[InputRequired()])
	password = PasswordField('Password', validators=[InputRequired(), 
		EqualTo('confirm', message = "Passwords must match")])
	confirm = PasswordField('Confirm Password')
