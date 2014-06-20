# -*- coding: utf-8 -*-
# ...

import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

WHOOSH_BASE = os.path.join(basedir, 'search.db')
# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

CSRF_ENABLED = True
SECRET_KEY = '\x84iiDQ\x82\x875\xc2\x9d\x13\x11\xfd\xb4\xa2\x91\x95\x85v\xf6o\xa3<\x9f'

POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50

