# -*- coding: utf-8 -*-
"""
    talkoohakemisto
    ~~~~~~~~~~~~~~~

    This module contains the Flask application core.
"""
import os
import warnings

import colander
from flask import Flask, jsonify, _request_ctx_stack
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm.exc import NoResultFound

from .extensions import db, mail, sentry


warnings.simplefilter('error', SAWarning)


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings(environment)
        self._init_extensions()
        self._init_blueprints()
        self._init_errorhandlers()
        self._init_request_hooks()

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
        from .views.type import type
        from .views.voluntary_work import voluntary_work

        self.register_blueprint(municipality)
        self.register_blueprint(type)
        self.register_blueprint(voluntary_work)

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

    def _init_errorhandlers(self):
        @self.errorhandler(400)
        def bad_request(error):
            return jsonify(message=u'Bad request'), 400

        @self.errorhandler(404)
        @self.errorhandler(NoResultFound)
        def object_not_found(error):
            return jsonify(message=u'Not found.'), 404

        @self.errorhandler(colander.Invalid)
        def invalid_data(error):
            errors = [
                {
                    'path': '/' + key.replace('.', '/'),
                    'reason': value
                }
                for key, value in error.asdict().iteritems()
            ]
            return jsonify(message=u'Validation failed', errors=errors), 400

    def _init_request_hooks(self):
        self.after_request(self._add_cors_headers)

    def _add_cors_headers(self, response):
        url_adapter = _request_ctx_stack.top.url_adapter

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ', '.join(
                url_adapter.allowed_methods()
            ),
            'Access-Control-Allow-Headers': ', '.join([
                'Accept',
                'Content-Type',
                'Origin',
                'X-Requested-With',
            ])
        }
        response.headers.extend(headers)

        return response
