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
    goal = u'Talkootyön tavoite'
    url = u'http://example.com'
    hashtag = u'#hashtag'
    location = u'Peruskoulu 2'
    time = u'11:00 - 20:00'
    contact_phone = u'+3585554444'
    organization = u'Järjestö'
    type = SubFactory(VoluntaryWorkTypeFactory)
    municipality = SubFactory(MunicipalityFactory)




