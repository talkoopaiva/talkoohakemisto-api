from flask import Blueprint\
    #, jsonify
from flask.ext.jsonpify import jsonify

from ..models import VoluntaryWorkType
from ..serializers import VoluntaryWorkTypeSerializer

type = Blueprint(
    name='type',
    import_name=__name__,
    url_prefix='/types'
)


@type.route('')
def index():
    types = (
        VoluntaryWorkType.query
        .order_by(VoluntaryWorkType.name)
        .all()
    )
    serializer = VoluntaryWorkTypeSerializer(types, many=True)
    return jsonify(types=serializer.data)


@type.route('/<int:id>')
def get(id):
    type = VoluntaryWorkType.query.filter_by(id=id).one()
    serializer = VoluntaryWorkTypeSerializer([type], many=True)
    return jsonify(types=serializer.data)
