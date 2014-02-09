# -*- coding: utf-8 -*-
from flask import json, url_for
import pytest

from talkoohakemisto import models, serializers
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


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkGetSingle(object):
    @pytest.fixture
    def voluntary_work(self):
        work = factories.VoluntaryWorkFactory()
        db.session.commit()
        return work

    @pytest.fixture
    def response(self, client, voluntary_work):
        return client.get(url_for('voluntary_work.get', id=voluntary_work.id))

    def test_url(self):
        assert url_for('voluntary_work.get', id=123) == '/voluntary_works/123'

    def test_returns_200(self, response):
        assert response.status_code == 200

    def test_returns_type_as_json(self, response, voluntary_work):
        serializer = serializers.VoluntaryWorkSerializer(
            [voluntary_work],
            many=True
        )
        assert response.json == {
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
                    [voluntary_work.municipality],
                    many=True
                ).data,
                'types': serializers.VoluntaryWorkTypeSerializer(
                    [voluntary_work.type],
                    many=True
                ).data,
            }
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkGetSingleWhenNotFound(object):
    @pytest.fixture
    def response(self, client):
        return client.get(url_for('voluntary_work.get', id=12345))

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkGetSingleWithNonIntegerID(object):
    @pytest.fixture
    def response(self, client):
        return client.get('/voluntary_works/foobar')

    def test_returns_404(self, response):
        assert response.status_code == 404

    def test_returns_error_as_json(self, response):
        assert response.json == {
            'message': 'Not found.'
        }


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkCreation(object):
    @pytest.fixture
    def type(self):
        type = factories.VoluntaryWorkTypeFactory()
        db.session.commit()
        return type

    @pytest.fixture
    def municipality(self):
        municipality = factories.MunicipalityFactory()
        db.session.commit()
        return municipality

    @pytest.fixture
    def data(self, municipality, type):
        return {
            'voluntary_works': [{
                'name': u'Fillareiden korjausta',
                'organizer': u'Matti Mallikas',
                'contact_email': u'matti@mallikas.fi',
                'street_address': u'Metsänneidonkuja 6',
                'description': u'Korjataan porukalla fillareita',
                'links': {
                    'municipality': municipality.code,
                    'type': type.id,
                }
            }]
        }

    @pytest.fixture
    def response(self, client, data):
        return client.post(
            '/voluntary_works',
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/vnd.api+json',
                'Accept': 'application/vnd.api+json',
            }
        )

    @pytest.fixture
    def voluntary_work(self, response):
        id = response.json['voluntary_works'][0]['id']
        return models.VoluntaryWork.query.get(id)

    def test_returns_201(self, response):
        assert response.status_code == 201

    def test_response_has_location_header(self, response, voluntary_work):
        url = url_for(
            'voluntary_work.get',
            id=voluntary_work.id,
            _external=True
        )
        assert response.location == url

    def test_saves_voluntary_work_to_database(
        self, data, voluntary_work, municipality, type
    ):
        data = data['voluntary_works'][0]
        assert voluntary_work.name == data['name']
        assert voluntary_work.organizer == data['organizer']
        assert voluntary_work.contact_email == data['contact_email']
        assert voluntary_work.street_address == data['street_address']
        assert voluntary_work.description == data['description']
        assert voluntary_work.municipality is municipality
        assert voluntary_work.type is type


@pytest.mark.usefixtures('request_ctx', 'database')
class TestVoluntaryWorkCreationWithInvalidData(object):
    @pytest.fixture
    def type(self):
        type = factories.VoluntaryWorkTypeFactory()
        db.session.commit()
        return type

    @pytest.fixture
    def data(self, type):
        return {
            'voluntary_works': [
                {
                    'name': u'Fillareiden korjausta',
                    'organizer': u'Matti Mallikas',
                    'contact_email': u'invalid',
                    'links': {
                        'municipality': 12345,
                        'type': type.id,
                    }
                }
            ]
        }

    @pytest.fixture
    def response(self, client, data):
        return client.post(
            '/voluntary_works',
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/vnd.api+json',
                'Accept': 'application/vnd.api+json',
            }
        )

    def test_returns_400(self, response):
        assert response.status_code == 400

    def test_returns_field_specific_errors(self, response):
        errors = response.json['errors']
        assert response.json['message'] == 'Validation failed'
        assert {
            'path': '/voluntary_works/0/contact_email',
            'reason': 'Invalid email address'
        } in errors
        assert {
            'path': '/voluntary_works/0/links/municipality',
            'reason': '12345 is not a valid municipality ID'
        } in errors

    def test_doesnt_save_anything_to_database(self, response):
        assert models.VoluntaryWork.query.count() == 0


class TestVoluntaryWorkCreationWithInvalidJSON(object):
    @pytest.fixture
    def response(self, client):
        return client.post(
            '/voluntary_works',
            data='{foobar',
            headers={
                'Content-Type': 'application/vnd.api+json',
                'Accept': 'application/vnd.api+json',
            }
        )

    def test_returns_400(self, response):
        assert response.status_code == 400

    def test_returns_proper_error_message(self, response):
        assert response.json == {'message': 'Bad request'}
