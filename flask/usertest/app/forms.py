from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
	emailAddress = EmailField('emailField')
	password = StringField('passwordField')

	