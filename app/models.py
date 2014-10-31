from app import db, app
from datetime import datetime
import re
from config import WHOOSH_ENABLED



authors = db.Table('authors',
	db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
	db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
	)

class User(db.Model):
	id = db.Column('user_id', db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, index=True)
	pw_hash = db.Column(db.String(100))

	def __init__(self, username, pw_hash):
		self.username = username
		self.pw_hash = pw_hash
	def __repr__(self):
		return '<User %r>' % self.username

	def is_authenticated(self): return True
	def is_active(self): return True
	def is_anonymous(self): return False
	def get_id(self): return unicode(self.id)


class Author(db.Model):
	__searchable__ = ['name']
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique=True, index = True)
	created = db.Column(db.DateTime, default = datetime.utcnow)
	
	def __init__(self, name):
		self.name = ' '.join([w.capitalize() for w in name.split(' ')]).strip()
		self.created = datetime.utcnow()
	def __repr__(self):
		return '<Author %r>' % self.name
		
	@classmethod
	def by_name(cls, name):
		name = ' '.join([w.capitalize() for w in name.split(' ')])
		return cls.query.filter_by(name = name).first()
	@classmethod
	def is_valid(cls, name):
		return name != '' and cls.by_name(name)


class Book(db.Model):
	__searchable__ = ['name']
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique=True, index = True)
	created = db.Column(db.DateTime, default = datetime.utcnow)
	authors = db.relationship('Author', secondary = authors,
		backref = db.backref('books', lazy = 'dynamic'))

	def __init__(self, name, authors):
		self.name = name.strip()
		self.authors = authors
		self.created = datetime.utcnow()


	def __repr__(self):
		return '<Book %r>' % self.name

if WHOOSH_ENABLED:
	import flask.ext.whooshalchemy as whooshalchemy
	whooshalchemy.whoosh_index(app, Book)
	whooshalchemy.whoosh_index(app, Author)



