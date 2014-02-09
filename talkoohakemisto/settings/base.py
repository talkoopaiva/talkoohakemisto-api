# -*- coding: utf-8 -*-
"""
    talkoohakemisto.settings.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains global application settings that are common to all
    environments.
"""
import os


#
# Paths
# -----

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)


#
# Generic
# -------

# Controls if the cookie should be set with the httponly flag. Defaults
# to ``True``.
SESSION_COOKIE_HTTPONLY = True


#
# Mail
# -----

MAIL_DEFAULT_SENDER = u'Talkoopäivä <info@talkoot.fi>'


#
# Sentry
# ------

# A sentry compatible DSN.
SENTRY_DSN = os.environ.get('SENTRY_DSN')
