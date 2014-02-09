import colander
import pytest

from talkoohakemisto import schemas
from . import factories


@pytest.mark.usefixtures('database')
class TestVoluntaryWorkLinkSchema(object):
    @pytest.fixture
    def schema(self):
        return schemas.VoluntaryWorkLinksSchema()

    @pytest.fixture
    def type(self):
        return factories.VoluntaryWorkTypeFactory()

    @pytest.fixture
    def municipality(self):
        return factories.MunicipalityFactory()

    def test_municipality_is_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['municipality'] == u'Required'

    def test_municipality_must_be_an_integer(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'municipality': 'foobar'})
        errors = excinfo.value.asdict()
        assert errors['municipality'] == u'"foobar" is not a number'

    def test_municipality_must_exist(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'municipality': 12345})
        errors = excinfo.value.asdict()
        assert (
            errors['municipality'] ==
            u'12345 is not a valid municipality ID'
        )

    def test_type_is_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['type'] == u'Required'

    def test_type_must_be_an_integer(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'type': 'foobar'})
        errors = excinfo.value.asdict()
        assert errors['type'] == u'"foobar" is not a number'

    def test_type_must_exist(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'type': 12345})
        errors = excinfo.value.asdict()
        assert errors['type'] == u'12345 is not a valid type ID'

    def test_valid_data(self, type, municipality, schema):
        data = schema.deserialize({
            'municipality': municipality.code,
            'type': type.id
        })
        assert data['type'] is type
        assert data['municipality'] is municipality


@pytest.mark.usefixtures('database')
class TestVoluntaryWorkSchema(object):
    @pytest.fixture
    def schema(self):
        return schemas.VoluntaryWorkSchema()

    @pytest.fixture
    def type(self):
        return factories.VoluntaryWorkTypeFactory()

    @pytest.fixture
    def municipality(self):
        return factories.MunicipalityFactory()

    def test_name_is_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['name'] == u'Required'

    def test_name_min_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'name': ''})
        errors = excinfo.value.asdict()
        assert errors['name'] == u'Required'

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'name': 'a'})
        errors = excinfo.value.asdict()
        assert 'name' not in errors

    def test_name_max_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'name': 100 * 'a'})
        errors = excinfo.value.asdict()
        assert 'name' not in errors

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'name': 101 * 'a'})
        errors = excinfo.value.asdict()
        assert errors['name'] == u'Longer than maximum length 100'

    def test_organizer_is_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['organizer'] == u'Required'

    def test_organizer_min_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'organizer': ''})
        errors = excinfo.value.asdict()
        assert errors['organizer'] == u'Required'

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'organizer': 'a'})
        errors = excinfo.value.asdict()
        assert 'organizer' not in errors

    def test_organizer_max_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'organizer': 100 * 'a'})
        errors = excinfo.value.asdict()
        assert 'organizer' not in errors

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'organizer': 101 * 'a'})
        errors = excinfo.value.asdict()
        assert errors['organizer'] == u'Longer than maximum length 100'

    def test_description_is_optional(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert 'description' not in errors

    def test_description_max_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'description': 1000 * 'a'})
        errors = excinfo.value.asdict()
        assert 'description' not in errors

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'description': 1001 * 'a'})
        errors = excinfo.value.asdict()
        assert errors['description'] == u'Longer than maximum length 1000'

    def test_street_address_is_optional(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert 'street_address' not in errors

    def test_street_address_max_length(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'street_address': 100 * 'a'})
        errors = excinfo.value.asdict()
        assert 'street_address' not in errors

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'street_address': 101 * 'a'})
        errors = excinfo.value.asdict()
        assert errors['street_address'] == u'Longer than maximum length 100'

    def test_contact_email_is_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['contact_email'] == u'Required'

    def test_contact_email_must_be_valid_email(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'contact_email': 'invalid'})
        errors = excinfo.value.asdict()
        assert errors['contact_email'] == u'Invalid email address'

    def test_contact_email_max_length(self, schema):
        domain = u'@example.com'

        def make_email(length):
            return (length - len(domain)) * 'a' + domain

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'contact_email': make_email(100)})
        errors = excinfo.value.asdict()
        assert 'contact_email' not in errors

        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'contact_email': make_email(101)})
        errors = excinfo.value.asdict()
        assert errors['contact_email'] == u'Longer than maximum length 100'

    def test_links_are_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['links'] == u'Required'

    def test_minimal_valid_data(self, type, municipality, schema):
        data = {
            'name': u'Fillareiden korjausta',
            'organizer': u'Matti Mallikas',
            'links': {
                'municipality': municipality.code,
                'type': type.id,
            },
            'contact_email': u'matti@mallikas.fi',
        }
        data = schema.deserialize(data)
        assert data['name'] == u'Fillareiden korjausta'
        assert data['organizer'] == u'Matti Mallikas'
        assert data['contact_email'] == u'matti@mallikas.fi'
        assert data['description'] == u''
        assert data['street_address'] == u''
        assert data['links']['type'] is type
        assert data['links']['municipality'] is municipality


@pytest.mark.usefixtures('database')
class TestVoluntaryWorkListSchema(object):
    @pytest.fixture
    def schema(self):
        return schemas.VoluntaryWorkListSchema()

    @pytest.fixture
    def type(self):
        return factories.VoluntaryWorkTypeFactory()

    @pytest.fixture
    def municipality(self):
        return factories.MunicipalityFactory()

    def test_voluntary_works_are_required(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({})
        errors = excinfo.value.asdict()
        assert errors['voluntary_works'] == u'Required'

    def test_min_voluntary_works(self, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({'voluntary_works': []})
        errors = excinfo.value.asdict()
        assert errors['voluntary_works'] == u'Shorter than minimum length 1'

    def test_max_voluntary_works(self, municipality, type, schema):
        with pytest.raises(colander.Invalid) as excinfo:
            schema.deserialize({
                'voluntary_works': [
                    {
                        'name': u'Fillareiden korjausta',
                        'organizer': u'Matti Mallikas',
                        'links': {
                            'municipality': municipality.code,
                            'type': type.id,
                        },
                        'contact_email': u'matti@mallikas.fi',
                    },
                    {
                        'name': u'Fillareiden korjausta',
                        'organizer': u'Matti Mallikas',
                        'links': {
                            'municipality': municipality.code,
                            'type': type.id,
                        },
                        'contact_email': u'matti@mallikas.fi',
                    },
                ]
            })
        errors = excinfo.value.asdict()
        assert errors['voluntary_works'] == u'Longer than maximum length 1'

    def test_minimal_valid_data(self, type, municipality, schema):
        data = {
            'voluntary_works': [{
                'name': u'Fillareiden korjausta',
                'organizer': u'Matti Mallikas',
                'links': {
                    'municipality': municipality.code,
                    'type': type.id,
                },
                'contact_email': u'matti@mallikas.fi',
            }]
        }
        data = schema.deserialize(data)
        data = data['voluntary_works'][0]
        assert data['name'] == u'Fillareiden korjausta'
        assert data['organizer'] == u'Matti Mallikas'
        assert data['contact_email'] == u'matti@mallikas.fi'
        assert data['description'] == u''
        assert data['street_address'] == u''
        assert data['links']['type'] is type
        assert data['links']['municipality'] is municipality
