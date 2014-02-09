# -*- coding: utf-8 -*-
from factory import Factory, Sequence, SubFactory

from talkoohakemisto import models
from talkoohakemisto.extensions import db


class SQLAlchemyModelFactory(Factory):
    ABSTRACT_FACTORY = True
    FACTORY_SESSION = db.session

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        obj = target_class(*args, **kwargs)
        db.session.add(obj)
        db.session.flush()
        return obj


class Factory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session


class MunicipalityFactory(Factory):
    FACTORY_FOR = models.Municipality
    code = Sequence(lambda n: n)
    name = Sequence(lambda n: u'Kunta {0}'.format(n))


class VoluntaryWorkTypeFactory(Factory):
    FACTORY_FOR = models.VoluntaryWorkType
    name = Sequence(lambda n: u'Tyyppi {0}'.format(n))


class VoluntaryWorkFactory(Factory):
    FACTORY_FOR = models.VoluntaryWork
    name = Sequence(lambda n: u'Talkoot {0}'.format(n))
    organizer = u'Pekka Perusjätkä'
    description = u'Talkootyön kuvaus'
    street_address = u'Metsänneidonkuja 6'
    contact_email = u'someone@example.com'
    type = SubFactory(VoluntaryWorkTypeFactory)
    municipality = SubFactory(MunicipalityFactory)
