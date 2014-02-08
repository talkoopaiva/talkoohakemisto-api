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

    def test_returns_municipalities_as_json(self, response, types):
        serializer = serializers.VoluntaryWorkTypeSerializer(
            types,
            many=True
        )
        assert response.json == {
            'types': serializer.data
        }
