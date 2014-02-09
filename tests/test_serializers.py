# -*- coding: utf-8 -*-
from talkoohakemisto import serializers
from tests import factories


def test_municipality_serializer():
    municipality = factories.MunicipalityFactory.build()
    serializer = serializers.MunicipalitySerializer(municipality)
    assert serializer.data == {
        'id': unicode(municipality.code),
        'name': municipality.name,
    }


def test_voluntary_work_type_serializer():
    type_ = factories.VoluntaryWorkTypeFactory.build(id=123)
    serializer = serializers.VoluntaryWorkTypeSerializer(type_)
    assert serializer.data == {
        'id': unicode(type_.id),
        'name': type_.name,
    }


def test_voluntary_work_serializer():
    work = factories.VoluntaryWorkFactory.build(id=123)
    work.type.id = 4
    work.municipality.code = 98
    serializer = serializers.VoluntaryWorkSerializer(work)
    assert serializer.data == {
        'id': u'123',
        'name': work.name,
        'organizer': u'Pekka Perusjätkä',
        'description': u'Talkootyön kuvaus',
        'street_address': u'Metsänneidonkuja 6',
        'contact_email': u'someone@example.com',
        'links': {
            'municipality': u'98',
            'type': u'4'
        }
    }
