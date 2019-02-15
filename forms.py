from wtforms import *
from wtforms.validators import *
from models import *

def login_free(form, field):
	login = field.data
	check = User.get(login=login)
	if check is not None:
		raise ValidationError('Login %r is already taken' % login)

def email_free(form, field):
	email = field.data
	check = User.get(email=email)
	if check is not None:
		raise ValidationError('E-mail %r is already in use' % email)

def len_check(form, field):
	pwd = field.data
	if len(pwd) < 5:
		raise ValidationError('Your password is too short, use 5 or more characters')

def pwd_check(form, field):
	pwd2 = field.data
	pwd1 = form.pwd1.data
	if pwd1 != pwd2:
		raise ValidationError('Passwords should match')

def login_check(form, field):
	login = field.data
	check = User.get(login=login)
	if check is None:
		raise ValidationError('User with login %r not found' % login)

def pwd_match_check(form, field):
	login = form.login.data
	pwd = field.data
	check = User.get(login=login, pwd=pwd)
	if check is None:
		raise ValidationError('Wrong password. Try again')

def dev_title_free(form, field):
	title = field.data
	check = User.get(login=title)
	if check is not None:
		raise ValidationError('Title is already in use')

def dev_email_free(form, field):
	email = field.data
	check = User.get(email=email)
	if check is not None:
		raise ValidationError('E-mail is already in use')

def dev_title_check(form, field):
	title = field.data
	check = User.get(login=title)
	if check is None:
		raise ValidationError('Title %r was not found' % title)

def dev_pwd_check(form, field):
	pwd = field.data
	dev = User.get(login=form.title.data)
	if dev.pwd != pwd:
		raise ValidationError('Password do not match. Try again')

def positive_integer_check(form, field):
	value = field.data
	try:
		v = int(value)
	except Exception:
		raise ValidationError('integer required')

	if v < 0:
		raise ValidationError('positive number required')

class RegForm(Form):
	login = StringField('Login', [InputRequired(), login_free])
	email = StringField('E-mail', [InputRequired(), email_free])
	pwd1 = PasswordField('Password', [InputRequired(), len_check])
	pwd2 = PasswordField('Password again', [InputRequired(), pwd_check])


class LoginForm(Form):
	login = StringField('Login', [InputRequired(), login_check])
	pwd = PasswordField('Password', [InputRequired(), pwd_match_check])


class DevRegForm(Form):
	title = StringField('Title', [InputRequired(), dev_title_free])
	email = StringField('E-mail', [InputRequired(), dev_email_free])
	pwd1 = PasswordField('Password', [InputRequired(), len_check])
	pwd2 = PasswordField('Password again', [InputRequired(), pwd_check])


class DevLoginForm(Form):
	title = StringField('Title', [InputRequired(), dev_title_check])
	pwd = PasswordField('Password', [InputRequired(), dev_pwd_check])


class DevNewGameForm(Form):
	title = StringField('Title', [InputRequired()])
	description = StringField('Description', [InputRequired()])
	genres = StringField('Genres', [InputRequired()])
	price = IntegerField('Price', [InputRequired(), positive_integer_check])
	small = StringField('Small', [InputRequired()])
	cover = StringField('Small', [InputRequired()])
	# image = FileField('Image')
