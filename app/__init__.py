from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')

# import logging
# import sys
# app.debug = True

# # Configure logging.
# app.logger.setLevel(logging.DEBUG)
# del app.logger.handlers[:]

# handler = logging.StreamHandler(stream=sys.stdout)
# handler.setLevel(logging.DEBUG)
# handler.formatter = logging.Formatter(
#     fmt=u"%(asctime)s level=%(levelname)s %(message)s",
#     datefmt="%Y-%m-%dT%H:%M:%SZ",
# )
# app.logger.addHandler(handler)

from app import views, models



