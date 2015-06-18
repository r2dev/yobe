from flask.ext.wtf import Form
from wtforms import SubmitField, TextField, PasswordField, validators, BooleanField, StringField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp
from ..models import User
class RegisterationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	
	username = StringField('Username', validators=[Required(), Length(1,64), 
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Invalid username')])
	password = PasswordField('New Password', 
		validators=[Required(), EqualTo('confirm', 'Passwords must match')])
	confirm = PasswordField('Repeat Password')
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already registered')

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Log in')
