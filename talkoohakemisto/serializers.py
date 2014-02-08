from marshmallow import fields, Serializer


class MunicipalitySerializer(Serializer):
    id = fields.String(attribute='code')

    class Meta:
        fields = ('id', 'name')


class VoluntaryWorkTypeSerializer(Serializer):
    id = fields.String()

    class Meta:
        fields = ('id', 'name')
