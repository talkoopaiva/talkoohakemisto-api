# -*- coding: utf-8 -*-
"""
    talkoohakemisto.settings.test
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains application settings specific to a automated tests.
"""

from .base import *  # flake8: noqa

#
# Generic
# -------

# If a secret key is set, cryptographic components can use this to sign cookies
# and other things. Set this to a complex random value when you want to use the
# secure cookie for instance.
SECRET_KEY = 'development key'

# The debug flag. Set this to True to enable debugging of the application. In
# debug mode the debugger will kick in when an unhandled exception ocurrs and
# the integrated server will automatically reload the application if changes in
# the code are detected.
DEBUG = True

TESTING = True


#
# Mail
# ----

MAIL_SUPPRESS_SEND = True


#
# SQLAlchemy
# ----------

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'TEST_DATABASE_URL',
    'postgres://localhost/talkoohakemisto_test'
) + os.environ.get('TEST_PROCESS_NUMBER', '')
