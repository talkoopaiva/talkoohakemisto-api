from .extensions import db


class Municipality(db.Model):
    __tablename__ = 'municipality'

    code = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name


class VoluntaryWorkType(db.Model):
    __tablename__ = 'voluntary_work_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name
