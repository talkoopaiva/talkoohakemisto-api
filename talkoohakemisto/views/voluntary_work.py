import operator

from flask import Blueprint, jsonify, request, url_for

from ..extensions import db
from ..models import VoluntaryWork
from ..schemas import VoluntaryWorkListSchema
from ..serializers import (
    MunicipalitySerializer,
    VoluntaryWorkSerializer,
    VoluntaryWorkTypeSerializer,
)

voluntary_work = Blueprint(
    name='voluntary_work',
    import_name=__name__,
    url_prefix='/voluntary_works'
)


@voluntary_work.route('')
def index():
    page = request.args.get('page', type=int, default=1)
    pagination = (
        VoluntaryWork.query
        .order_by(VoluntaryWork.id)
        .paginate(page=page)
    )
    return jsonify(**_serialize_pagination(pagination))


@voluntary_work.route('/<int:id>')
def get(id):
    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()
    return jsonify(**_serialize([voluntary_work]))


@voluntary_work.route('', methods=['POST'])
def post():
    schema = VoluntaryWorkListSchema()

    data = schema.deserialize(request.get_json(force=True))
    data = data['voluntary_works'][0]
    data.update(data.pop('links'))

    voluntary_work = VoluntaryWork(**data)
    db.session.add(voluntary_work)
    db.session.commit()

    response = jsonify(**_serialize([voluntary_work]))
    response.status_code = 201
    response.location = url_for('.get', id=voluntary_work.id)
    return response


def _get_links():
    return {
        'voluntary_works.municipality': {
            'href': (
                url_for('municipality.index', _external=True) +
                '/{voluntary_works.municipality}'
            ),
            'type': 'municipalities'
        },
        'voluntary_works.type': {
            'href': (
                url_for('type.index', _external=True) +
                '/{voluntary_works.type}'
            ),
            'type': 'types'
        }
    }


def _get_linked(voluntary_works):
    relationships = [
        ('type', 'types', 'id', VoluntaryWorkTypeSerializer),
        ('municipality', 'municipalities', 'code', MunicipalitySerializer),
    ]
    linked = {}
    for name, plural_name, primary_key, serializer_cls in relationships:
        items = set(getattr(work, name) for work in voluntary_works)
        items = sorted(items, key=operator.attrgetter(primary_key))
        serializer = serializer_cls(items, many=True)
        linked[plural_name] = serializer.data
    return linked


def _serialize(voluntary_works):
    serializer = VoluntaryWorkSerializer(voluntary_works, many=True)
    return {
        'links': _get_links(),
        'voluntary_works': serializer.data,
        'linked': _get_linked(voluntary_works)
    }


def _serialize_pagination(pagination):
    data = _serialize(pagination.items)
    data['meta'] = {
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'total': pagination.total,
        }
    }
    return data
