# -*- coding: utf-8 -*-
import pytest

from talkoohakemisto import services
from talkoohakemisto.extensions import mail
from . import factories


@pytest.mark.usefixtures('database')
class TestVoluntaryWorkConfirmationService(object):
    @pytest.fixture
    def voluntary_work(self):
        return factories.VoluntaryWorkFactory(id=123)

    @pytest.fixture
    def expected_code(self):
        return 'MTIz.2y16vOnURswWiVWkpHsS414wiag'

    @pytest.fixture
    def expected_url(self, expected_code):
        return 'https://hakemisto.talkoot.fi/123/muokkaa/' + expected_code

    @pytest.fixture
    def service(self, voluntary_work):
        return services.VoluntaryWorkEmailConfirmationService(
            voluntary_work.id
        )

    def test_get_editing_code(self, service, expected_code):
        assert service.get_editing_code() == expected_code

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
        assert expected_url in msg.body
