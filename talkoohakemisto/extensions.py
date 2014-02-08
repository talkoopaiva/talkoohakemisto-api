from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

db = SQLAlchemy()
mail = Mail()
sentry = Sentry()
