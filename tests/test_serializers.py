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
