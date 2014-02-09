from flask import url_for
import pytest

from talkoohakemisto import serializers
from talkoohakemisto.extensions import db
from tests import factories


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkIndex(object):
    @pytest.fixture
    def types(self):
        types = [
            factories.VoluntaryWorkTypeFactory(),
            factories.VoluntaryWorkTypeFactory(),
        ]
        db.session.commit()
        return types

    @pytest.fixture
    def municipalities(self):
        municipalities = [
            factories.MunicipalityFactory(),
            factories.MunicipalityFactory(),
        ]
        db.session.commit()
        return municipalities

    @pytest.fixture
    def works(self, municipalities, types):
        works = [
            factories.VoluntaryWorkFactory(
                municipality=municipalities[0],
                type=types[0]
            ),
            factories.VoluntaryWorkFactory(
                municipality=municipalities[1],
                type=types[0]
            ),
            factories.VoluntaryWorkFactory(
                municipality=municipalities[0],
                type=types[1]
            ),
        ]
        db.session.commit()
        return works

    @pytest.fixture
    def response(self, client, works):
        return client.get(url_for('voluntary_work.index'))

    def test_url(self):
        assert url_for('voluntary_work.index') == '/voluntary_works'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_returns_voluntary_works_as_json(
        self, response, municipalities, types, works
    ):
        serializer = serializers.VoluntaryWorkSerializer(
            works,
            many=True
        )
        assert response.json == {
            'meta': {
                'pagination': {
                    'page': 1,
                    'pages': 1,
                    'total': 3,
                    'per_page': 20
                }
            },
            'links': {
                'voluntary_works.municipality': {
                    'href': (
                        'http://localhost/municipalities'
                        '/{voluntary_works.municipality}'
                    ),
                    'type': 'municipalities'
                },
                'voluntary_works.type': {
                    'href': (
                        'http://localhost/types'
                        '/{voluntary_works.type}'
                    ),
                    'type': 'types'
                }
            },
            'voluntary_works': serializer.data,
            'linked': {
                'municipalities': serializers.MunicipalitySerializer(
                    municipalities,
                    many=True
                ).data,
                'types': serializers.VoluntaryWorkTypeSerializer(
                    types,
                    many=True
                ).data,
            }
        }
