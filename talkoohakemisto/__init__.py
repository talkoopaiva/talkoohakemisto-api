# -*- coding: utf-8 -*-
"""
    talkoohakemisto
    ~~~~~~~~~~~~~~~

    This module contains the Flask application core.
"""
import os
import warnings

from flask import Flask
from sqlalchemy.exc import SAWarning

from .extensions import db, mail, sentry


warnings.simplefilter('error', SAWarning)


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings(environment)
        self._init_extensions()
        self._init_blueprints()

    def _init_settings(self, environment=None):
        """
        Initialize application configuration.

        This method loads the configuration from the given environment
        (production, development, test).  If no environment is given as an
        argument, the environment is read from ``FLASK_ENV`` environmental
        variable.  If ``FLASK_ENV`` is not defined, the environment defaults to
        development.

        The environment specific configuration is loaded from the module
        corresponding to the environment in :module:`.settings`.

        :param environment: the application environment
        """
        if environment is None:
            environment = os.environ.get('FLASK_ENV', 'development')
        settings_module = 'talkoohakemisto.settings.' + environment
        self.config.from_object(settings_module)

    def _init_blueprints(self):
        from .views.municipality import municipality
        self.register_blueprint(municipality)

    def _init_extensions(self):
        """Initialize and configure Flask extensions with this application."""
        db.init_app(self)
        mail.init_app(self)
        self._init_raven()

    def _init_raven(self):
        from raven.conf import EXCLUDE_LOGGER_DEFAULTS, setup_logging
        from raven.handlers.logging import SentryHandler

        # Initialize Raven only if SENTRY_DSN setting is defined.
        if not self.config.get('SENTRY_DSN'):
            return

        sentry.init_app(self)
        handler = SentryHandler(sentry.client)

        setup_logging(handler, exclude=EXCLUDE_LOGGER_DEFAULTS + (
            'celery',
            'newrelic',
            'requests',
        ))
