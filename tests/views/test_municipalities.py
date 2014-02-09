from flask import url_for
import pytest

from talkoohakemisto import serializers
from talkoohakemisto.extensions import db
from tests import factories


@pytest.mark.usefixtures('request_ctx', 'database')
class TestMunicipalityIndex(object):
    @pytest.fixture
    def municipalities(self):
        municipalities = [
            factories.MunicipalityFactory(),
            factories.MunicipalityFactory(),
        ]
        db.session.commit()
        return municipalities

    @pytest.fixture
    def response(self, client, municipalities):
        return client.get(url_for('municipality.index'))

    def test_url(self):
        assert url_for('municipality.index') == '/municipalities'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_returns_municipalities_as_json(self, response, municipalities):
        serializer = serializers.MunicipalitySerializer(
            municipalities,
            many=True
        )
        assert response.json == {
            'municipalities': serializer.data
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestMunicipalityGetSingle(object):
    @pytest.fixture
    def municipality(self):
        municipality = factories.MunicipalityFactory()
        db.session.commit()
        return municipality

    @pytest.fixture
    def response(self, client, municipality):
        return client.get(url_for('municipality.get', id=municipality.code))

    def test_url(self):
        assert url_for('municipality.get', id=123) == '/municipalities/123'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_returns_municipality_as_json(self, response, municipality):
        serializer = serializers.MunicipalitySerializer(
            [municipality],
            many=True
        )
        assert response.json == {
            'municipalities': serializer.data
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestMunicipalityGetSingleWhenNotFound(object):
    @pytest.fixture
    def response(self, client):
        return client.get(url_for('municipality.get', id=12345))

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestMunicipalityGetSingleWithNonIntegerID(object):
    @pytest.fixture
    def response(self, client):
        return client.get('/municipalities/foobar')

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }
