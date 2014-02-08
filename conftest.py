import os

from flask import _request_ctx_stack, json, Response
import pytest
from werkzeug import cached_property

from talkoohakemisto import Application
from talkoohakemisto.extensions import db


def _get_process_number(config):
    SLAVE_ID_PREFIX_LENGTH = 2
    try:
        slaveid = config.slaveinput['slaveid']
    except AttributeError:
        zero_based_process_number = 0
    else:
        zero_based_process_number = int(slaveid[SLAVE_ID_PREFIX_LENGTH:])
    return zero_based_process_number + 1


def _set_process_number_to_env(config):
    number = _get_process_number(config)
    os.environ['TEST_PROCESS_NUMBER'] = '' if number == 1 else str(number)


def pytest_configure(config):
    _set_process_number_to_env(config)


class TestResponse(Response):
    @cached_property
    def json(self):
        return json.loads(self.data)


@pytest.fixture(scope='session')
def app(request):
    app = Application('test')
    app.response_class = TestResponse

    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@pytest.yield_fixture
def request_ctx(request, app):
    ctx = app.test_request_context()
    ctx.push()
    yield ctx
    if _request_ctx_stack.top and _request_ctx_stack.top.preserved:
        _request_ctx_stack.top.pop()
    ctx.pop()


@pytest.fixture(scope='session')
def client(request, app):
    return app.test_client()


@pytest.fixture(scope='session')
def dbschema(request, app):
    db.create_all()
    request.addfinalizer(db.drop_all)


@pytest.yield_fixture
def database(app, dbschema):
    yield

    db.session.remove()

    # Delete all data from tables.
    tables = reversed(db.metadata.sorted_tables)
    for table in tables:
        db.session.execute(table.delete())
    db.session.commit()

    db.session.close_all()
    db.engine.dispose()
