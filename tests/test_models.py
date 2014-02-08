# -*- coding: utf-8 -*-
from .factories import MunicipalityFactory


class TestMunicipality(object):
    def test_unicode(self):
        municipality = MunicipalityFactory.build()
        assert unicode(municipality) == municipality.name

    def test_str(self):
        municipality = MunicipalityFactory.build(name=u'Mäntyharju')
        assert str(municipality) == 'Mäntyharju'

    def test_repr(self):
        municipality = MunicipalityFactory.build()
        assert repr(municipality) == '<Municipality {0!r}>'.format(
            municipality.name
        )
