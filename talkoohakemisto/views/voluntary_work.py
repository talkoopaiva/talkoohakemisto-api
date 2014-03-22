import operator

from flask import abort, Blueprint, request, Response, url_for, json
from flask.ext.jsonpify import jsonify
#from flask import jsonify
import jsonpatch

from ..extensions import db
from ..models import VoluntaryWork
from ..schemas import VoluntaryWorkListSchema
from ..serializers import (
    MunicipalitySerializer,
    VoluntaryWorkSerializer,
    VoluntaryWorkTypeSerializer,
)
from ..services import (
    VoluntaryWorkEditTokenService,
    VoluntaryWorkEmailConfirmationService
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
        .order_by(db.desc(VoluntaryWork.id))
        .paginate(page=page)
    )
    return jsonify(**_serialize_pagination(pagination))


@voluntary_work.route('/<int:id>')
def get(id):
    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()
    return jsonify(**_serialize([voluntary_work]))

"""
#@voluntary_work.route('', methods=['POST'])
def post():

    schema = VoluntaryWorkListSchema()

    try:
        data = schema.deserialize(request.get_json(force=True))
    except Exception as inst:
        print inst

    data = data['voluntary_works'][0]
    data.update(data.pop('links'))

    voluntary_work = VoluntaryWork(**data)
    db.session.add(voluntary_work)

    db.session.commit()

    service = VoluntaryWorkEmailConfirmationService(voluntary_work.id)
    service.send_confirmation_email()
    token = VoluntaryWorkEditTokenService.get_token(voluntary_work.id)
    voluntary_work['token'] = token

    response = jsonify(**_serialize([voluntary_work]))
    response.status_code = 201
    response.location = url_for('.get', id=voluntary_work.id)
    return response
"""
@voluntary_work.route('/create')
def post():

    schema = VoluntaryWorkListSchema()
    print request.args['data']

    print 1
    try:
        data = schema.deserialize(json.loads(request.args['data']))
    except Exception as inst:
        print "EXCEPTION"
        print inst

    print 2

    data = data['voluntary_works'][0]
    data.update(data.pop('links'))
    print 3

    voluntary_work = VoluntaryWork(**data)
    db.session.add(voluntary_work)
    print 4

    db.session.commit()
    print 5

    service = VoluntaryWorkEmailConfirmationService(voluntary_work.id)
    service.send_confirmation_email()
    print 6

    token = VoluntaryWorkEditTokenService.get_token(voluntary_work.id)
    print 7

    ser = _serialize([voluntary_work])
    #ser['voluntary_works']['token'] = token
    print ser['voluntary_works'][0].update({"token": token})

    print 8
    response = jsonify(**ser)
    response.status_code = 201
    response.location = url_for('.get', id=voluntary_work.id)
    return response


@voluntary_work.route('/<int:id>', methods=['PATCH'])
def patch(id):
    if request.mimetype != 'application/json-patch+json':
        abort(400)

    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()
    edit_token = request.args.get('edit_token', '')
    voluntary_work_id = (
        VoluntaryWorkEditTokenService
        .get_voluntary_work_id_from_token(edit_token)
    )

    if voluntary_work.id != voluntary_work_id:
        abort(403)

    serializer = VoluntaryWorkSerializer([voluntary_work], many=True)
    json = {'voluntary_works': serializer.data}
    try:
        patch = jsonpatch.JsonPatch(request.get_json(force=True))
    except Exception as es:
        print es

    patch.apply(json, in_place=True)

    schema = VoluntaryWorkListSchema()
    data = schema.deserialize(json)
    data = data['voluntary_works'][0]
    data.update(data.pop('links'))

    for key, value in data.iteritems():
        setattr(voluntary_work, key, value)
    db.session.commit()

    return Response(mimetype='application/json', status=204)


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
