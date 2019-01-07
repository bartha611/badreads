from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email

class Registration(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=10, max=70), Email("must provide a valid email between 10 to 70 characters")])
	password = PasswordField('password', validators=[InputRequired(), 
		EqualTo('confirm', message = "Passwords must match")])
	confirm = PasswordField('Confirm Password')
	submit = SubmitField('Submit')

class Login(FlaskForm):
	username = StringField('username', validators = [InputRequired(), Length(min=10, max=70), Email("must provide a valid email between 10 to 70 characters")])
	password = PasswordField('Password', validators = [InputRequired()])
	submit = SubmitField('Submit')

class SearchForm(FlaskForm):
	search = StringField('search', validators = [InputRequired()], render_kw = {"placeholder": "Search"})
	submit = SubmitField('Submit')
