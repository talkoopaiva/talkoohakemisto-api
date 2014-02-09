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


class VoluntaryWork(db.Model):
    __tablename__ = 'voluntary_work'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), nullable=False)
    organizer = db.Column(db.Unicode(100), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)
    street_address = db.Column(db.Unicode(100), nullable=False)
    contact_email = db.Column(db.Unicode(100), nullable=False)
    type_id = db.Column(
        None,
        db.ForeignKey(VoluntaryWorkType.id),
        nullable=False
    )
    municipality_code = db.Column(
        None,
        db.ForeignKey(Municipality.code),
        nullable=False
    )

    type = db.relationship(VoluntaryWorkType)
    municipality = db.relationship(Municipality)

    @property
    def links(self):
        return {
            'municipality': self.municipality.code,
            'type': self.type.id
        }

    def __repr__(self):
        return '<{0} {1!r}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name
