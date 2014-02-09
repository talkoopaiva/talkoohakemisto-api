# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from talkoohakemisto.extensions import db

from .factories import (
    MunicipalityFactory,
    VoluntaryWorkFactory,
    VoluntaryWorkTypeFactory
)


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


class TestVoluntaryWork(object):
    def test_unicode(self):
        work = VoluntaryWorkFactory.build()
        assert unicode(work) == work.name

    def test_str(self):
        work = VoluntaryWorkTypeFactory.build(name=u'Työpaja')
        assert str(work) == 'Työpaja'

    def test_repr(self):
        work = VoluntaryWorkFactory.build()
        assert repr(work) == '<VoluntaryWork {0!r}>'.format(work.name)

    def test_name_cannot_be_null(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(name=None)

    def test_organizer_cannot_be_null(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(organizer=None)

    def test_description_cannot_be_null(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(description=None)

    def test_street_address_cannot_be_null(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(street_address=None)

    def test_contact_email_cannot_be_null(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(contact_email=None)

    def test_type_cannot_be_none(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(type=None)

    def test_cannot_delete_referred_type(self, database):
        work = VoluntaryWorkFactory()
        db.session.delete(work.type)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_municipality_cannot_be_none(self, database):
        with pytest.raises(IntegrityError):
            VoluntaryWorkFactory(municipality=None)

    def test_cannot_delete_referred_municipality(self, database):
        work = VoluntaryWorkFactory()
        db.session.delete(work.municipality)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_created_at_is_automatically_set_to_current_time(self, database):
        work = VoluntaryWorkFactory()
        timediff = datetime.utcnow() - work.created_at
        assert timediff < timedelta(seconds=1)

    def test_created_at_cannot_be_none(self, database):
        work = VoluntaryWorkFactory()
        work.created_at = None
        with pytest.raises(IntegrityError):
            db.session.commit()
