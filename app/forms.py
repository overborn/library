from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, FieldList, BooleanField, FormField
from wtforms.validators import Required, Length, EqualTo

class LoginForm(Form):
	username = TextField('username', validators = [Required(), Length(min = 3, max = 18)])
	password = PasswordField('password', validators = [Required(), Length(min = 8, max = 18)])

class SignupForm(Form):
	username = TextField('username', validators = [Required(), Length(min=3, max = 18)])
	password = PasswordField('password', validators = [Required(),
		Length(min = 8, max = 18), 
		EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('confirm')

	# def validate(self):
	# 	if not Form.validate(self):
	# 		return False
	# 	if self.username.data != User.make_valid_nickname(self.username.data):
	# 		self.username.errors.append(gettext('''This nickname has invalid characters.
	# 			Please use letters, numbers, dots and underscores only.'''))
	# 		return False
	# 	return True

class SearchForm(Form):
	search = TextField('search', validators = [Required()])
	by_title = BooleanField(default = True, label='Search by title')
	by_author = BooleanField(default = False, label='Search by author')
	def validate(self):
		if not Form.validate(self):
			return False
		if not self.by_title.data and not self.by_author.data:			
			return False
		return True

class EditAuthor(Form):
	name = TextField('name', validators = [Required()])

class AddAuthor(Form):
	name = TextField('name', validators = [Required()])

class EditBook(Form):
	title = TextField('title', validators = [Required()])
	authors = FieldList(TextField('authors'), min_entries=1, max_entries=8)





