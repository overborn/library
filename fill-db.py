from app.models import Book, Author
from app import db
import random, string

NUMBER_OF_ENTITIES = 500
NAMES = ['Jayme', 'Cyrus', 'Branden', 'Lara', 'Ian', 'Garret', 'Ursa', 'Moses', 'Eleonor',
'Jacob', 'Homer', 'Blythe', 'Freya', 'Summer', 'Gabriel', 'Brody', 'Seth', 'Alice', 'Ivor',
'Eleanor', 'Jaime', 'Adam', 'Odysseus', 'Charlotte', 'Thomas', 'Zahir', 'Elmo', 'Bradley',
'Conan', 'Ann', 'Ria', 'Tanek', 'Aladdin', 'Garrett', 'Acton', 'Jane', 'John', 'Mary',
'Burke', 'Martha', 'Aubrey', 'Jenna', 'Lunea', 'Reed', 'Zelenia', 'Dahlia', 'Olaf', 'Xerxes',
'Susan', 'Bill', 'Nina', 'Phoebe', 'Hasad', 'Wilma', 'Stephanie', 'Madison', 'Kylee',
'Clinton', 'Yeo', 'Josephine', 'Jade', 'Owen', 'Jennifer', 'Steve', 'Flavia', 'Dorothy',
'Jared', 'Macaulay', 'Amery', 'Sonya', 'Tom', 'Isaac', 'Jackson', 'Ruth', 'Bob', 'Riley',
'Jemima', 'Elvis', 'Megan', 'Tiger', 'Vernon', 'Rhiannon', 'Herman', 'Erich', 'Kennedy',
'Olga', 'Trevor', 'Erica', 'Anastasia', 'Austin', 'Maxine', 'Chadwick', 'Jenny', 'Craig',
'Preston', 'Rob', 'Lillith', 'Wade', 'Peter', 'Ivy', 'Indira', 'Ralph', 'Jerry', 'Tim',
'Tanya', 'Hope', 'Odessa', 'Albert', 'Faith', 'Alex', 'Edan', 'Lavinia', 'Ingrid', 'Ivan',
'Karleigh', 'Stewart', 'Signe', 'Karyn', 'Julie', 'Bertha', 'Quinn', 'Melvin', 'Linus',
'Xanthus']
SURNAMES = ['Gonzalez', 'Gonzales', 'Smith', 'Dudley', 'Weiss', 'Montgomery', 'Hayden',
'Hill', 'Olson', 'Moses', 'Potts', 'Powell', 'Rosario', 'William', 'Dunn', 'Brooks',
'Flores', 'Barber', 'Swanson', 'Maddox', 'Crane', 'Strong', 'Atkins', 'Mayson', 'Vasquez',
'Michael', 'Eaton', 'Mcbride', 'Jacobson', 'Thomas', 'Moore', 'Schwartz', 'Barnett', 'Russo',
'George', 'Little', 'Jackson', 'Sparks', 'Long', 'Noel', 'Sloan', 'White', 'Hopkins', 'Ross',
'Whitaker', 'Sweeney', 'Tucker', 'Davidson', 'Cline', 'Johnson', 'Blackburn', 'Baker', 'Neal',
'Kortez', 'Chang', 'Warner', 'Fischer', 'Evans', 'Chan', 'Bowen', 'Middleton', 'Cameron',
'Dawson', 'Rivera', 'Donaldson', 'Manson', 'Fuller', 'Horton', 'Riley', 'Lambert', 'Floyd',
'Garza', 'Hanson', 'Knowles', 'Alexander', 'Kennedy', 'Delacruz', 'Collman', 'Hayes',
'Mcfarland', 'Rivas', 'Cortez', 'Bauer', 'Austin', 'Fernandez', 'Taller', 'Wall', 'Leon',
'Crosby', 'Wade', 'Blankenship', 'Maynard', 'Romero', 'Pearson', 'Pugh', 'Shields', 'Mueller',
'Raymond', 'Jordan', 'Goff', 'Grinberg', 'Stevenson', 'Pierce', 'Rios', 'Reid', 'Banks',
'Becker', 'Conrad', 'Mitchell', 'Gazmanov', 'Patterson', 'Gates', 'Miller', 'Colon', 'Wolf']

WORDS = ['Story', 'Tale', 'Trip', 'Quest', 'Saga', 'House', 'Man', 'Problem', 'Salvation',
'Pain', 'Redemption', 'Mice', 'Life', 'Matter', 'Game', 'Deal', 'Trouble', 'Lies', 'Journey',
'Parade', 'Circus', 'Love', 'Betrayal', 'Faith', 'Home', 'Cross', 'Headache', 'Headway', 'Path',
'Way', 'Highway', 'Book', 'Promise', 'Habbit', 'Dream', 'Vision', 'Prison', 'Soldier', 'Guide',
'River', 'Lake', 'Holy', 'Shop', 'Town', 'City', 'Park', 'Hill', 'Bottom', 'Barrel', 'Kiss',
'Play', 'Mirror', 'Grey', 'Wall', 'Well', 'Veil', 'Beast', 'Thrill', 'Art', 'Boom', 'Word',
'World', 'Road', 'Star', 'Farewell', 'Loss', 'Eye', 'Fist', 'Point']

PREPS = [' by', ' and', ' for', ' with', ' of', ' without']
authorNames = set([])
bookNames = set([])
while len(authorNames) < NUMBER_OF_ENTITIES:
	name = random.choice(NAMES) + random.choice([' ', ' ' + random.choice(
		string.ascii_uppercase) + '. ']) + random.choice(SURNAMES)
	authorNames.add(name)

while len(bookNames) < NUMBER_OF_ENTITIES:
	name = random.choice([''] * 4 + [random.choice(NAMES) + "'s "]) + random.choice(
		WORDS) + random.choice([' '] * 6 + PREPS) + ' ' + ' '.join(random.sample(
			WORDS, random.randint(0,2)))
	bookNames.add(name)

for name in authorNames:
	db.session.add(Author(name))

db.session.commit()
authors = Author.query.all()

for name in bookNames:
	db.session.add(Book(name, random.sample(authors, random.randint(1,5))))
	
db.session.commit()



