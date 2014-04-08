from flask import Blueprint
    #, jsonify
from flask.ext.jsonpify import jsonify

from ..models import Municipality
from ..serializers import MunicipalitySerializer

municipality = Blueprint(
    name='municipality',
    import_name=__name__,
    url_prefix='/municipalities'
)


@municipality.route('')
def index():
    municipalities = Municipality.query.order_by(Municipality.name).all()
    serializer = MunicipalitySerializer(municipalities, many=True)
    return jsonify(municipalities=serializer.data)


@municipality.route('/<int:id>')
def get(id):
    municipality = Municipality.query.filter_by(code=id).one()
    serializer = MunicipalitySerializer([municipality], many=True)
    return jsonify(municipalities=serializer.data)
