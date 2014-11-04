from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, FieldList, BooleanField, FormField
from wtforms.validators import Required, Length, EqualTo
# from models import Book

class LoginForm(Form):
	username = TextField('username', validators = [Required(), Length(min = 3, max = 18)])
	password = PasswordField('password', validators = [Required(), Length(min = 8, max = 18)])

class SignupForm(Form):
	username = TextField('username', validators = [Required(), Length(min=3, max = 18)])
	password = PasswordField('password', validators = [Required(),
		Length(min = 8, max = 18), 
		EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('confirm')

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

class AddBook(Form):
	title = TextField('title', validators = [Required()])
	authors = FieldList(TextField('authors'), min_entries=1, max_entries=8)

class BetterFieldList(FieldList):
	def __init__(self, *args, **kwargs):
		self.book = kwargs.pop("book", None)
		if self.book:
			self.min_entries = len(self.book.authors)
		super(BetterFieldList, self).__init__(*args, **kwargs)

class EditBook(Form):
	title = TextField('title', validators = [Required()])
	authors = FieldList(TextField(), min_entries=1, max_entries=8)	
	def __init__(self, *args, **kwargs):
		super(EditBook, self).__init__(*args, **kwargs)
		self.book = kwargs.pop("book", None)
		self.title.data = self.book.name
		self.authors[0].data = self.book.authors[0].name
		# for a in self.book.authors[1:]:
		# 	self.authors.append_entry(a.name)
		#self.process(obj=self.book)
				
		# if self.book:			
			#self.authors.min_entries = len(self.book.authors)
			#self.authors.entries = [a.name for a in self.book.authors]
		
		# if not self.book:
		# 	super(EditBook, self).__init__(*args, **kwargs)
			#raise ValueError("requires book to be set")
