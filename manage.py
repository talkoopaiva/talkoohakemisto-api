#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os

from flask import current_app
from flask.ext.failsafe import failsafe
from flask.ext.script import Manager, Server


@failsafe
def create_app():
    from talkoohakemisto import Application
    return Application()


manager = Manager(create_app)
manager.add_command('runserver', Server(host='37.139.26.202'))


@manager.shell
def make_shell_context():
    from talkoohakemisto.extensions import db

    context = {}
    context['app'] = current_app
    context['db'] = db
    context.update(db.Model._decl_class_registry)

    return context


@manager.command
def generate_secret_key():
    """Generate a good unique secret key."""
    print base64.b64encode(os.urandom(40))


if __name__ == '__main__':
    manager.run()
