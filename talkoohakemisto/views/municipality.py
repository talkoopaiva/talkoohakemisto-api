from flask import Blueprint, jsonify

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
