from flask import current_app, render_template
from flask.ext.mail import Message
from itsdangerous import URLSafeSerializer

from .extensions import mail
from .models import VoluntaryWork


class VoluntaryWorkEditTokenService(object):
    @staticmethod
    def get_serializer():
        return URLSafeSerializer(
            current_app.secret_key,
            salt='edit-voluntary-work'
        )

    @classmethod
    def get_token(cls, voluntary_work_id):
        return cls.get_serializer().dumps(voluntary_work_id)

    @classmethod
    def get_voluntary_work_id_from_token(cls, token):
        return cls.get_serializer().loads(token)


class VoluntaryWorkEmailConfirmationService(object):
    def __init__(self, voluntary_work_id):
        self.voluntary_work = VoluntaryWork.query.get(voluntary_work_id)

    def get_editing_url(self):
        return u'https://hakemisto.talkoot.fi/{id}/edit/{token}'.format(
            id=self.voluntary_work.id,
            token=VoluntaryWorkEditTokenService.get_token(
                self.voluntary_work.id
            )
        )

    def send_confirmation_email(self):
        message = Message(
            recipients=[self.voluntary_work.contact_email],
            subject=u'Kiitos talkoiden ilmoittamisesta!',
            body=render_template(
                'emails/voluntary_work_created.txt',
                edit_url=self.get_editing_url()
            )
        )
        mail.send(message)
