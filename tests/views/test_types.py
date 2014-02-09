from flask import url_for
import pytest

from talkoohakemisto import serializers
from talkoohakemisto.extensions import db
from tests import factories


@pytest.mark.usefixtures('request_ctx', 'database')
class TestTypeIndex(object):
    @pytest.fixture
    def types(self):
        types = [
            factories.VoluntaryWorkTypeFactory(),
            factories.VoluntaryWorkTypeFactory(),
        ]
        db.session.commit()
        return types

    @pytest.fixture
    def response(self, client, types):
        return client.get(url_for('type.index'))

    def test_url(self):
        assert url_for('type.index') == '/types'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_response_has_proper_content_type(self, response):
        assert response.mimetype == 'application/vnd.api+json'

    def test_returns_types_as_json(self, response, types):
        serializer = serializers.VoluntaryWorkTypeSerializer(
            types,
            many=True
        )
        assert response.json == {
            'types': serializer.data
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestTypeGetSingle(object):
    @pytest.fixture
    def type(self):
        type = factories.VoluntaryWorkTypeFactory()
        db.session.commit()
        return type

    @pytest.fixture
    def response(self, client, type):
        return client.get(url_for('type.get', id=type.id))

    def test_url(self):
        assert url_for('type.get', id=123) == '/types/123'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_response_has_proper_content_type(self, response):
        assert response.mimetype == 'application/vnd.api+json'

    def test_returns_type_as_json(self, response, type):
        serializer = serializers.VoluntaryWorkTypeSerializer(
            [type],
            many=True
        )
        assert response.json == {
            'types': serializer.data
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestTypeGetSingleWhenNotFound(object):
    @pytest.fixture
    def response(self, client):
        return client.get(url_for('type.get', id=12345))

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_response_has_proper_content_type(self, response):
        assert response.mimetype == 'application/vnd.api+json'

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestTypeGetSingleWithNonIntegerID(object):
    @pytest.fixture
    def response(self, client):
        return client.get('/types/foobar')

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_response_has_proper_content_type(self, response):
        assert response.mimetype == 'application/vnd.api+json'

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }
