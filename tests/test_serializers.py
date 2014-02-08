from talkoohakemisto import serializers
from tests import factories


def test_municipality_serializer():
    municipality = factories.MunicipalityFactory.build()
    serializer = serializers.MunicipalitySerializer(municipality)
    assert serializer.data == {
        'id': unicode(municipality.code),
        'name': municipality.name,
    }
