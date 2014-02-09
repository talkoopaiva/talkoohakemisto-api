# -*- coding: utf-8 -*-
"""
    talkoohakemisto.settings.production
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains application settings specific to a production
    environment running on Heroku.
"""

import os

from .base import *  # flake8: noqa

#
# Generic
# -------

# If a secret key is set, cryptographic components can use this to sign cookies
# and other things. Set this to a complex random value when you want to use the
# secure cookie for instance.
SECRET_KEY = os.environ['SECRET_KEY']

# The debug flag. Set this to True to enable debugging of the application. In
# debug mode the debugger will kick in when an unhandled exception ocurrs and
# the integrated server will automatically reload the application if changes in
# the code are detected.
DEBUG = 'DEBUG' in os.environ

# Controls if the cookie should be set with the secure flag. Defaults
# to ``False``.
SESSION_COOKIE_SECURE = True


#
# SQLAlchemy
# ----------

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


#
# Email configuration
# -------------------

MAIL_SERVER = 'smtp.mandrillapp.com'
MAIL_USERNAME = os.environ['MANDRILL_USERNAME']
MAIL_PASSWORD = os.environ['MANDRILL_APIKEY']
MAIL_PORT = 587
MAIL_USE_TLS = True
