from factory.alchemy import SQLAlchemyModelFactory

from pywatch.extensions import db


class Factory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session
