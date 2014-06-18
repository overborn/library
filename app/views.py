from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from forms import LoginForm, SearchForm, SignupForm, EditAuthor, EditBook, AddBook
from models import User, Book, Author
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
import hashlib, re, random, string

def make_salt(): return ''.join(random.choice(string.letters) for x in xrange(5))
def make_pw_hash(name, pw, salt=None):
    if not salt: salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)
def valid_pw(name, pw, h): return h == make_pw_hash(name, pw, h.split('|')[1])
def valid_username(username): return re.match(r'^[a-zA-Z0-9_-]{3,18}', username)

def author_by_name(name):
	name = ' '.join([w.capitalize() for w in name.split(' ')])
	return Author.query.filter_by(name = name).first()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect(url_for('search_results', query = form.search.data))
	return render_template('search.html', form = form)

@app.route('/search_results/<query>')
def search_results(query):
	results = []
	form = SearchForm()
	if form.by_title:
		results += Book.query.whoosh_search(
			"*" + query + "*", limit = MAX_SEARCH_RESULTS, fields=('name',)).all()
	print results
	if form.by_author:
		authors = Author.query.whoosh_search(
			"*" + query + "*", limit = MAX_SEARCH_RESULTS).all()
		res = set([])
		for author in authors:
			res.update(author.books)
		results += list(res)
		results = list(set(results))
	
	print query, results
	return render_template('search_results.html', query = query, results = results)


@app.route('/signup', methods=['GET','POST'])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():
		username = form.username.data
		if not valid_username(username):
			flash('Invalid username, try another one.')
			return render_template('signup.html', form = form)
		registered_user = User.query.filter_by(username=username).first()
		if registered_user:
			flash('User already exists, try another username')
			return render_template('signup.html', form = form)
		password = form.password.data
		pw = make_pw_hash(username, password)
		user = User(username, pw)
		db.session.add(user)
		db.session.commit()
		flash('User successfully registered')
		return redirect(url_for('login'))
	return render_template('signup.html', form = form)


@app.route('/login', methods=['GET','POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data		
		registered_user = User.query.filter_by(username=username).first()
		if registered_user is None or not valid_pw(
			username, password, registered_user.pw_hash):
			flash('Username or password is invalid')
			return redirect(url_for('login'))
		login_user(registered_user)
		flash('Logged in successfully')
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/books', methods = ['GET', 'POST'])
@app.route('/books/<int:page>', methods = ['GET', 'POST'])
def books(page = 1):
	books = Book.query.order_by(Book.created.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('books.html', books = books)


@app.route('/authors', methods = ['GET', 'POST'])
@app.route('/authors/<int:page>', methods = ['GET', 'POST'])
def authors(page = 1):
	authors = Author.query.order_by(Author.created.desc()).paginate(page, POSTS_PER_PAGE, False)
	print authors.items
	return render_template('authors.html', authors = authors)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/author/add', methods = ['GET', 'POST'])
@login_required
def add_author():
	form = EditAuthor()
	if form.validate_on_submit():
		name = form.name.data
		registered_author = author_by_name(name)
		if registered_author:
			flash('Author already exists.')
			return redirect(url_for('add_author'))
		author = Author(name)
		db.session.add(author)
		db.session.commit()
		flash("You've added a new author.")
		return redirect(url_for('authors'))
	return render_template('add_author.html', form = form)




@app.route('/author/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_author(id):
	author = Author.query.get(id)
	if author == None:
		flash("Author is not found")
		return redirect(url_for('authors'))
	form = EditAuthor()
	if form.validate_on_submit():
		name = form.name.data
		if author_by_name(name) and author_by_name(name).id != author.id:
			flash("Can't change name to existing one.")
			return redirect(url_for('edit_author', id = id))
		author.name = name
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_author', id = id))
	form.name.data = author.name
	return render_template('edit_author.html', form = form)

@app.route('/author/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_author(id):
	author = Author.query.get(id)
	if author == None:
		flash("Author is not found")
		return redirect(url_for('index'))
	db.session.delete(author)
	db.session.commit()
	flash("Author has been deleted")
	return redirect(url_for('authors'))

@app.route('/book/add', methods = ['GET', 'POST'])
@login_required
def add_book():
	form = AddBook()
	if form.validate_on_submit():		
		title = form.data['title']
		book = Book.query.filter_by(name=title).first()
		if book:
			flash('Book already exists.')
			return redirect(url_for('edit_book', id = book.id))
		authors = list(set([author_by_name(
			name=a) for a in form.data['authors'] if a and author_by_name(name=a)]))		
		book = Book(title, authors)
		db.session.add(book)
		db.session.commit()
		flash('Book has been added.')
		return redirect(url_for('books'))
	print form.data['authors']
	return render_template('add_book.html', form = form)

@app.route('/book/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_book(id):
	book = Book.query.get(id)
	if book == None:
		flash("Book is not found")
		return redirect(url_for('books'))
	print book.authors
	form = EditBook()
	#form.authors.min_entries = len(book.authors)
	form.title.data = book.name
	print form.authors.data
	form.authors[0].data = book.authors[0].name
	for author in book.authors[1:]:
		form.authors.append_entry(author.name)	
	print form.authors.data

	if form.validate_on_submit():		
		print form.data['authors']
		print request.data + 'lol'
		name = form.data['title']
		if id != Book.query.filter_by(name=name).first().id:
			flash("Can't change name to existing one.")
			return redirect(url_for('edit_book', id = id))
		book.name = name
		authors = list(set([author_by_name(
			name=a) for a in form.data['authors'] if a and author_by_name(name=a)]))
		#print authors
		book.authors = authors		
		db.session.commit()
		flash('Changes have been saved.')
		return redirect(url_for('edit_book', id=id))
	return render_template('edit_book.html', form = form)


@app.route('/book/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_book(id):
	book = Book.query.get(id)
	if book == None:
		flash("Book is not found")
		return redirect(url_for('books'))
	db.session.delete(book)
	db.session.commit()
	flash("Book has been deleted")
	return redirect(url_for('books'))