from flask import current_app, render_template
from flask.ext.mail import Message
from itsdangerous import URLSafeSerializer

from .extensions import mail
from .models import VoluntaryWork


class VoluntaryWorkEmailConfirmationService(object):
    def __init__(self, voluntary_work_id):
        self.voluntary_work = VoluntaryWork.query.get(voluntary_work_id)

    def get_serializer(self):
        return URLSafeSerializer(
            current_app.secret_key,
            salt='edit-voluntary-work'
        )

    def get_editing_code(self):
        serializer = self.get_serializer()
        return serializer.dumps(self.voluntary_work.id)

    def get_editing_url(self):
        return u'https://hakemisto.talkoot.fi/{id}/muokkaa/{code}'.format(
            id=self.voluntary_work.id,
            code=self.get_editing_code()
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
