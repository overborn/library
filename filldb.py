from app.models import User, Book, Author
from app import db
from datetime import datetime

b1 = Author('Oleg Gazmanov', datetime.utcnow())
b2 = Author('Gazman Olegov', datetime.utcnow())
b3 = Author('Taras Shevchenko', datetime.utcnow())
db.session.add(b1)
db.session.add(b2)
db.session.add(b3)


a1 = Book('Officer', [b1], datetime.utcnow())
a2 = Book('Esaul', [b1,b2], datetime.utcnow())
a3 = Book('Kobzar', [b3], datetime.utcnow())

db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.commit()
