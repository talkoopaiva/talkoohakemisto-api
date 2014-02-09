from marshmallow import fields, Serializer


class MunicipalitySerializer(Serializer):
    id = fields.String(attribute='code')

    class Meta:
        fields = ('id', 'name')


class VoluntaryWorkTypeSerializer(Serializer):
    id = fields.String()

    class Meta:
        fields = ('id', 'name')


class VoluntaryWorkLinksSerializer(Serializer):
    municipality = fields.String()
    type = fields.String()

    class Meta:
        fields = ('municipality', 'type')


class VoluntaryWorkSerializer(Serializer):
    id = fields.String()
    links = fields.Nested(VoluntaryWorkLinksSerializer)

    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'organizer',
            'contact_email',
            'street_address',
            'links'
        )
