from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# if os.environ.get('HEROKU') is not None:
#     import logging
#     stream_handler = logging.StreamHandler()
#     app.logger.addHandler(stream_handler)
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('microblog startup')

from app import views, models



