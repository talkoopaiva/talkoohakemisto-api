# -*- coding: utf-8 -*-
import pytest

from talkoohakemisto.services import (
    VoluntaryWorkEditTokenService,
    VoluntaryWorkEmailConfirmationService
)
from talkoohakemisto.extensions import mail
from . import factories


class TestVoluntaryWorkEditTokenService(object):
    @pytest.fixture
    def expected_token(self):
        return 'MTIz.2y16vOnURswWiVWkpHsS414wiag'

    def test_get_token(self, expected_token):
        token = VoluntaryWorkEditTokenService.get_token(123)
        assert token == 'MTIz.2y16vOnURswWiVWkpHsS414wiag'

    def test_get_voluntary_id_from_token(self):
        voluntary_work_id = (
            VoluntaryWorkEditTokenService.get_voluntary_work_id_from_token(
                'MTIz.2y16vOnURswWiVWkpHsS414wiag'
            )
        )
        assert voluntary_work_id == 123


@pytest.mark.usefixtures('database')
class TestVoluntaryWorkConfirmationService(object):
    @pytest.fixture
    def voluntary_work(self):
        return factories.VoluntaryWorkFactory(id=123)

    @pytest.fixture
    def expected_token(self):
        return 'MTIz.2y16vOnURswWiVWkpHsS414wiag'

    @pytest.fixture
    def expected_url(self, expected_token):
        return 'https://hakemisto.talkoot.fi/123/muokkaa/' + expected_token

    @pytest.fixture
    def service(self, voluntary_work):
        return VoluntaryWorkEmailConfirmationService(voluntary_work.id)

    def test_get_editing_url(self, service, expected_url):
        assert service.get_editing_url() == expected_url

    def test_send_confirmation_email(
        self, voluntary_work, service, expected_url
    ):
        with mail.record_messages() as outbox:
            service.send_confirmation_email()

        assert len(outbox) == 1

        msg = outbox[0]
        assert msg.subject == u'Kiitos talkoiden ilmoittamisesta!'
        assert msg.sender == u'Talkoopäivä <info@talkoot.fi>'
        assert msg.recipients == [voluntary_work.contact_email]
