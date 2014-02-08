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
