import flask
from flask import request
from flask.views import MethodView
from wtforms import Form, StringField, IntegerField, FloatField, validators, ValidationError
import wtforms_json
import lager
from tinydb import TinyDB

log=lager.Lager('events.json')
app = flask.Flask(__name__, static_folder='../../build')
wtforms_json.init()

class BeerForm(Form):
    name = StringField('name', [validators.Length(max=64), validators.DataRequired()])
    description = StringField('description', [validators.Length(max=1024), validators.DataRequired()])
    brewedBy = StringField('brewedBy', [validators.Length(max=64), validators.DataRequired()])
    style = StringField('style', [validators.Length(max=64), validators.DataRequired()])
    abv = FloatField('ABV', [validators.NumberRange(min=0, max=100)])
    FloatField('rating', [validators.NumberRange(min=0, max=100)])
    FloatField('IBU', [validators.NumberRange(min=0, max=300)])
    FloatField('SRM', [validators.NumberRange(min=0, max=100)])
    FloatField('costPerPint')
    #TODO: list of ratings?

class UserForm(Form):
    StringField('name', [validators.Length(max=25), validators.DataRequired()])
    StringField('email', [validators.Email()])
    StringField('rfidId', [validators.Length(max=35)])
    StringField('nfcId', [validators.Length(max=35)])
    StringField('untappedName', [validators.Length(max=35)])
    #TODO: list of pour ids?

class KegForm(Form):
    beerId = IntegerField('beerId', [validators.DataRequired()])
    litersRemaining = FloatField('litersRemaining', [])
    litersCapacity = FloatField('litersCapacity', [validators.DataRequired()])
    #TODO: validate litersRemaining < litersCapacity

class KegeratorForm(Form):
    StringField('name', [validators.Length(max=64)])
    IntegerField('kegIds', [])
    FloatField('desiredTemperatureC', [validators.NumberRange(min=-20, max=50)])

class ResourceApi(MethodView):
    def __init__(self, dbPath, resource_name, form_validator):
        super(ResourceApi, self).__init__()
        self.db = TinyDB(dbPath)
        self.resource_name = resource_name
        self.form_validator = form_validator

    def get(self, id):
        if id is None:
            # return a list of all resources
            return flask.jsonify({'data': self.db.all()})
        else:
            # expose a single resource
            match = self.db.get(eid=id)
            if match is None:
                flask.abort(404)
            return flask.jsonify(match)

    def post(self):
        # create a new resource
        form = self.form_validator.from_json(request.get_json())
        if form.validate():
            return flask.jsonify({'id':self.db.insert(form.data)})
        else:
            return flask.jsonify(form.errors), 400

    def delete(self, id):
        # delete a single resource
        try:
            self.db.remove(eids=[id])
            return flask.jsonify({'status': 'OK'})
        except KeyError:
            flask.abort(404)

    def partial_validate(self, form):
        ok = True
        errors = []
        for f in form:
            ok = ok and f.validate(form)
            errors.append(f.errors)
        return ok, {'errors': errors}

    def put(self, id):
        # update a single resource
        form = self.form_validator.from_json(request.get_json())
        valid, errors = self.partial_validate(form)
        if valid:
            value = self.db.get(eid=id)
            delta = {k: v for k,v in form.data.items() if v is not None}
            self.db.update(delta, eids=[id])
            return flask.jsonify(self.db.get(eid=id))
        else:
            return flask.jsonify(errors), 400


class BeerApi(ResourceApi):
    def __init__(self):
        super(BeerApi, self).__init__('beers.json', 'beers', BeerForm)


class UserApi(ResourceApi):
    def __init__(self):
        super(UserApi, self).__init__('users.json', 'users', UserForm)


class KegApi(ResourceApi):
    def __init__(self):
        super(KegApi, self).__init__('kegs.json', 'kegs', KegForm)


class KegeratorApi(MethodView):
    def __init__(self):
        super(KegeratorApi, self).__init__()
        self.db = TinyDB('kegerator.json')
        self.resource_name = "kegerator"
        self.form_validator = KegeratorForm
        if len(self.db.all()) == 0:
            self.db.insert({'name':'untitled',
                            'desiredTemperatureC':4.0,
                            'keg_ids': [0, 1]
                            })

    def get(self):
        # return kegerator data
        kegeratorState = self.db.all()[0]
        #TODO: pull this from sensors
        latestSensors = log.find_events(lager.Event.sensors, 'now')
        if len(latestSensors):
            kegeratorState.update(latestSensors[0]['data'])
        return flask.jsonify(kegeratorState)

    def put(self, id):
        # update thermostat
        form = KegeratorForm.from_json(request.get_json())
        valid, errors = self.partial_validate(form)
        if valid:
            value = self.db.get(eid=id)
            delta = {k: v for k,v in form.data.items() if v is not None}
            self.db.update(delta, eids=[id])
            #TODO apply this to the thermostat
            return flask.jsonify(self.db.get(eid=id))
        else:
            return flask.jsonify(errors), 400

class EventApi(MethodView):
    def get(self):
        types = request.args.get('types')
        start = request.args.get('startTime')
        end = request.args.get('endTime')
        # return matching event data
        events = log.find_events(types, start, end)
        return flask.jsonify({'events':events})

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(BeerApi, 'beers', '/beers/', pk='id')
register_api(UserApi, 'users', '/users/', pk='id')
register_api(KegApi, 'kegs', '/kegs/', pk='id')
app.add_url_rule('/kegerator/', view_func=KegeratorApi.as_view('kegerator'), methods=['GET','PUT'])
app.add_url_rule('/events/', view_func=EventApi.as_view('events'), methods=['GET'])

app.run(host='0.0.0.0', debug=True)