from app.models import User, Book, Author
from app import db

for book in Book.query.all(): db.session.delete(book)
for a in Author.query.all(): db.session.delete(a)
db.session.commit()
