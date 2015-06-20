from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, validators
from wtforms.validators import Required
class PostForm(Form):
	body = StringField("Enter something", validators=[Required()])
	submit = SubmitField('Submit')