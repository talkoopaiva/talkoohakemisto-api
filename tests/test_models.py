# -*- coding: utf-8 -*-
from .factories import MunicipalityFactory, VoluntaryWorkTypeFactory


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


class TestVoluntaryWorkType(object):
    def test_unicode(self):
        type_ = VoluntaryWorkTypeFactory.build()
        assert unicode(type_) == type_.name

    def test_str(self):
        type_ = VoluntaryWorkTypeFactory.build(name=u'Työpaja')
        assert str(type_) == 'Työpaja'

    def test_repr(self):
        type_ = VoluntaryWorkTypeFactory.build()
        assert repr(type_) == '<VoluntaryWorkType {0!r}>'.format(type_.name)
