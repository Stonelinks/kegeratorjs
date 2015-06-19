#!/usr/bin/env python3
import flask
import flask.views
import wtforms
import wtforms_json
import lager
import tinydb

log=lager.Lager('events.json')
app = flask.Flask(__name__, static_folder='../../build')
wtforms_json.init()

class BeerForm(wtforms.Form):
    name = wtforms.StringField('name', [wtforms.validators.Length(max=64),
                                        wtforms.validators.DataRequired()])
    description = wtforms.StringField('description', [wtforms.validators.Length(max=1024),
                                                      wtforms.validators.DataRequired()])
    brewedBy = wtforms.StringField('brewedBy', [wtforms.validators.Length(max=64),
                                                wtforms.validators.DataRequired()])
    style = wtforms.StringField('style', [wtforms.validators.Length(max=64),
                                          wtforms.validators.DataRequired()])
    abv = wtforms.FloatField('ABV', [wtforms.validators.NumberRange(min=0, max=100)])
    wtforms.FloatField('rating', [wtforms.validators.NumberRange(min=0, max=100)])
    wtforms.FloatField('IBU', [wtforms.validators.NumberRange(min=0, max=300)])
    wtforms.FloatField('SRM', [wtforms.validators.NumberRange(min=0, max=100)])
    wtforms.FloatField('costPerPint')
    #TODO: list of ratings?

class UserForm(wtforms.Form):
    wtforms.StringField('name', [wtforms.validators.Length(max=25),
                                 wtforms.validators.DataRequired()])
    wtforms.StringField('email', [wtforms.validators.Email()])
    wtforms.StringField('rfidId', [wtforms.validators.Length(max=35)])
    wtforms.StringField('nfcId', [wtforms.validators.Length(max=35)])
    wtforms.StringField('untappedName', [wtforms.validators.Length(max=35)])
    #TODO: list of pour ids?

class KegForm(wtforms.Form):
    beerId = wtforms.IntegerField('beerId', [wtforms.validators.DataRequired()])
    litersRemaining = wtforms.FloatField('litersRemaining', [])
    litersCapacity = wtforms.FloatField('litersCapacity', [wtforms.validators.DataRequired()])
    #TODO: validate litersRemaining < litersCapacity

class KegeratorForm(wtforms.Form):
    wtforms.StringField('name', [wtforms.validators.Length(max=64)])
    wtforms.IntegerField('kegIds', [])
    wtforms.FloatField('desiredTemperatureC', [wtforms.validators.NumberRange(min=-20, max=50)])

class ResourceApi(flask.views.MethodView):
    def __init__(self, dbPath, resource_name, form_validator):
        super(ResourceApi, self).__init__()
        self.db = tinydb.TinyDB(dbPath)
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
        form = self.form_validator.from_json(flask.request.get_json())
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

    def put(self, id):
        # update a single resource
        value = self.db.get(eid=id)
        value.update(flask.request.get_json())
        form = self.form_validator.from_json(value)
        if form.validate():
            self.db.update(form.data, eids=[id])
            return flask.jsonify(self.db.get(eid=id))
        else:
            return flask.jsonify(form.errors), 400


class BeerApi(ResourceApi):
    def __init__(self):
        super(BeerApi, self).__init__('beers.json', 'beers', BeerForm)


class UserApi(ResourceApi):
    def __init__(self):
        super(UserApi, self).__init__('users.json', 'users', UserForm)


class KegApi(ResourceApi):
    def __init__(self):
        super(KegApi, self).__init__('kegs.json', 'kegs', KegForm)


class KegeratorSettingsApi(flask.views.MethodView):
    def __init__(self):
        super(KegeratorSettingsApi, self).__init__()
        self.db = tinydb.TinyDB('kegerator.json')
        self.resource_name = "kegerator"
        self.form_validator = KegeratorForm
        if len(self.db.all()) == 0:
            self.db.insert({'name':'untitled',
                            'thermostat.setTempC':4.0,
                            'kegIds': [0, 1]
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
        form = KegeratorForm.from_json(flask.request.get_json())
        valid, errors = self.partial_validate(form)
        if valid:
            value = self.db.get(eid=id)
            delta = {k: v for k,v in form.data.items() if v is not None}
            self.db.update(delta, eids=[id])
            #TODO apply this to the thermostat
            return flask.jsonify(self.db.get(eid=id))
        else:
            return flask.jsonify(errors), 400


class SensorsApi(flask.views.MethodView):
    def get(self):
        # return kegerator sensor data
        latest_sensors = log.find_events(lager.Event.sensors, 'now')
        return flask.jsonify(latest_sensors)


class EventApi(flask.views.MethodView):
    def get(self):
        types = flask.request.args.get('types')
        start = flask.request.args.get('startTime')
        end = flask.request.args.get('endTime')
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

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)

register_api(BeerApi, 'beers', '/beers/', pk='id')
register_api(UserApi, 'users', '/users/', pk='id')
register_api(KegApi, 'kegs', '/kegs/', pk='id')
app.add_url_rule('/sensors/', view_func=SensorsApi.as_view('sensors'), methods=['GET'])
app.add_url_rule('/kegerator/', view_func=KegeratorSettingsApi.as_view('kegerator'), methods=['GET','PUT'])
app.add_url_rule('/events/', view_func=EventApi.as_view('events'), methods=['GET'])

app.run(host='0.0.0.0', debug=True)