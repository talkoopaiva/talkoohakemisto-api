# -*- coding: utf-8 -*-
from talkoohakemisto import serializers
from tests import factories
import json


def test_municipality_serializer():
    municipality = factories.MunicipalityFactory.build()
    serializer = serializers.MunicipalitySerializer(municipality)
    assert serializer.data == {
        'id': municipality.code,
        'name': municipality.name,
    }


def test_voluntary_work_type_serializer():
    type_ = factories.VoluntaryWorkTypeFactory.build(id=123)
    serializer = serializers.VoluntaryWorkTypeSerializer(type_)
    assert serializer.data == {
        'id': type_.id,
        'name': type_.name,
    }


def test_voluntary_work_serializer():
    work = factories.VoluntaryWorkFactory.build(id=123)
    work.type.id = 4
    work.municipality.code = 98
    serializer = serializers.VoluntaryWorkSerializer(work)

    assert json.dumps(serializer.data) == '{"description": "Talkooty\u00f6n kuvaus"' \
                                          ', "links": {"type": 4, "municipality": 98}, ' \
                                          '"url": "http://example.com", ' \
                                          '"goal": "Talkooty\u00f6n tavoite", ' \
                                          '"time": "11:00 - 20:00", ' \
                                          '"location": "Peruskoulu 2", ' \
                                          '"hashtag": "#hashtag", ' \
                                          '"organization": "J\u00e4rjest\u00f6", ' \
                                          '"organizer": "Pekka Perusj\u00e4tk\u00e4", ' \
                                          '"contact_phone": "+3585554444", ' \
                                          '"id": 123, ' \
                                          '"street_address": ' \
                                          '"Mets\u00e4nneidonkuja 6", ' \
                                          '"name": "' + work.name + '"}'