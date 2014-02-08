from factory import Factory, Sequence

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
