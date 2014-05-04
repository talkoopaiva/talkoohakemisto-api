import operator

from pprint import pprint

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
    VoluntaryWorkEditSerializer,
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
        .paginate(page=page, per_page=200)
    )
    return jsonify(**_serialize_pagination(pagination))


@voluntary_work.route('/<int:id>')
def get(id):
    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()
    return jsonify(**_serialize([voluntary_work]))

@voluntary_work.route('/edit/<int:id>')
def editget(id):
    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()
    return jsonify(**_serialize_edit([voluntary_work]))

@voluntary_work.route('', methods=['POST'])
def post3():

    schema = VoluntaryWorkListSchema()

    data = schema.deserialize(json.loads(request.data))
    data = data['voluntary_works'][0]
    data.update(data.pop('links'))

    voluntary_work = VoluntaryWork(**data)
    db.session.add(voluntary_work)

    db.session.commit()
    service = VoluntaryWorkEmailConfirmationService(voluntary_work.id)
    service.send_confirmation_email()

    token = VoluntaryWorkEditTokenService.get_token(voluntary_work.id)

    ser = _serialize([voluntary_work])
    #ser['voluntary_works'].update({"token": token})

    response = jsonify(**ser)
    response.status_code = 201
    response.location = url_for('.get', id=voluntary_work.id)
    return response


@voluntary_work.route('/create')
def post():

    schema = VoluntaryWorkListSchema()

    try:
        data = json.loads(request.data)
        #data = schema.deserialize(json.loads(request.args['data']))
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

    ser = _serialize([voluntary_work])
    #ser['voluntary_works']['token'] = token

    response = jsonify(**ser)
    response.status_code = 201
    response.location = url_for('.get', id=voluntary_work.id)
    return response


@voluntary_work.route('/<int:id>', methods=['POST'])
def post2(id):
#    if request.mimetype != 'application/json-patch+json':
#        abort(400)

    voluntary_work = VoluntaryWork.query.filter_by(id=id).one()

    data = json.loads(request.data)

    edit_token = data['voluntary_works'][0]['token']

    voluntary_work_id = (VoluntaryWorkEditTokenService.get_voluntary_work_id_from_token(edit_token))

    if voluntary_work.id != voluntary_work_id:
        abort(403)

    serializer = VoluntaryWorkEditSerializer([voluntary_work], many=True)
    json2 = {'voluntary_works': serializer.data}

    try:
        patch = jsonpatch.JsonPatch(data)
    except Exception as es:
        print es

    data = data['voluntary_works'][0]
    data.pop('links')
    data.pop('token')

    try:
        for key, value in data.iteritems():
            setattr(voluntary_work, key, value)
        db.session.commit()
    except Exception as es:
        abort(403)

    #return Response(mimetype='application/json', status=204)
    ser = _serialize([voluntary_work])

    response = jsonify(**ser)
    response.status_code = 200
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

def _serialize_edit(voluntary_works):
    serializer = VoluntaryWorkEditSerializer(voluntary_works, many=True)
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
