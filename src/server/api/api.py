#!/usr/bin/env python3
import flask
import flask.views
import wtforms
import wtforms_json
import tinydb
import werkzeug
import ike
import os.path
import config

global ike_instance

class BeerForm(wtforms.Form):
    name = wtforms.StringField('name', [wtforms.validators.Length(max=64),
                                        wtforms.validators.DataRequired()])
    description = wtforms.StringField('description', [wtforms.validators.Length(max=1024),
                                                      wtforms.validators.DataRequired()])
    brewedBy = wtforms.StringField('brewedBy', [wtforms.validators.Length(max=64),
                                                wtforms.validators.DataRequired()])
    style = wtforms.StringField('style', [wtforms.validators.Length(max=64),
                                          wtforms.validators.DataRequired()])
    abv = wtforms.FloatField('abv', [wtforms.validators.NumberRange(min=0, max=100)])
    rating = wtforms.FloatField('rating', [wtforms.validators.NumberRange(min=0, max=100)])
    ibu = wtforms.FloatField('ibu', [wtforms.validators.NumberRange(min=0, max=300)])
    srm = wtforms.FloatField('srm', [wtforms.validators.NumberRange(min=0, max=100)])
    costPerPint = wtforms.FloatField('costPerPint')
    #TODO: date on tap
    #TODO finished
    #TODO: list of ratings?


class UserForm(wtforms.Form):
    name = wtforms.StringField('name', [wtforms.validators.Length(max=25),
                                 wtforms.validators.DataRequired()])
    email = wtforms.StringField('email', [wtforms.validators.Email()])
    rfidId = wtforms.StringField('rfidId', [wtforms.validators.Length(max=35)])
    nfcId = wtforms.StringField('nfcId', [wtforms.validators.Length(max=35)])
    untappedName = wtforms.StringField('untappedName', [wtforms.validators.Length(max=35)])
    #TODO: list of pour ids?


class KegForm(wtforms.Form):
    beerId = wtforms.IntegerField('beerId', [wtforms.validators.DataRequired()])
    consumedL = wtforms.FloatField('consumedL', [])
    capacityL = wtforms.FloatField('capacityL', [wtforms.validators.DataRequired()])
    #TODO: validate litersRemaining < litersCapacity


class KegeratorForm(wtforms.Form):
    name = wtforms.StringField('name', [wtforms.validators.Length(max=64)])
    kegIds = wtforms.FieldList(wtforms.IntegerField('kegIds', []))


class ThermostatForm(wtforms.Form):
    setPointDegC = wtforms.FloatField('setPointDegC', [wtforms.validators.NumberRange(min=-20, max=50)])
    deadBandDegC = wtforms.FloatField('deadBandDegC', [wtforms.validators.NumberRange(min=0, max=10)])
    onAddsHeat = wtforms.BooleanField('onAddsHeat')


class ResourceApi(flask.views.MethodView):
    def __init__(self, dbPath, resource_name, form_validator):
        super(ResourceApi, self).__init__()
        self.db = tinydb.TinyDB(dbPath)
        self.resource_name = resource_name
        self.form_validator = form_validator

    def get(self, id):
        if id is None:
            # return a list of all resources
            match = self.db.all()
            for m in match:
                m['id'] = m.eid
        else:
            # expose a single resource
            match = self.db.get(eid=id)
            if match is None:
                raise werkzeug.exceptions.NotFound()
            else:
                match['id'] = id

        return flask.jsonify(match)

    def post(self):
        # create a new resource
        form = self.form_validator.from_json(flask.request.get_json())
        if form.validate():
            #TODO reject duplicate data
            if self.checkDataDuplicate(form.data):
                raise werkzeug.exceptions.BadRequest(flask.jsonify({"errors":"duplicate data not allowed"}))
            ret = flask.jsonify({'id':self.db.insert(form.data)})
        else:
            print(form.errors)
            raise werkzeug.exceptions.BadRequest(flask.jsonify(form.errors))
        return ret

    def delete(self, id):
        # delete a single resource
        try:
            self.db.remove(eids=[id])
            return flask.jsonify({'status': 'OK'})
        except KeyError:
            raise werkzeug.exceptions.NotFound()

    def put(self, id):
        # update a single resource
        value = self.db.get(eid=id)
        value.update(flask.request.get_json())
        form = self.form_validator.from_json(value)
        if form.validate():
            self.db.update(form.data, eids=[id])
            return flask.jsonify(self.db.get(eid=id))
        else:
            raise werkzeug.exceptions.BadRequest(flask.jsonify(form.errors))

    def checkDataDuplicate(self, data):
        pass

class BeerApi(ResourceApi):
    def __init__(self):
        super(BeerApi, self).__init__(os.path.join(config.DB_ROOT, 'beers.json'), 'beers', BeerForm)

class UserApi(ResourceApi):
    def __init__(self):
        super(UserApi, self).__init__(os.path.join(config.DB_ROOT, 'users.json'), 'users', UserForm)

    def checkDataDuplicate(self, data):
        return len(self.db.search(tinydb.where('email') == data['email']))>0

class KegApi(flask.views.MethodView):
    def get(self, id):
        try:
            return flask.jsonify(ike_instance._kegManager.dispatch(id, 'get_state'))
        except KeyError:
            raise werkzeug.exceptions.NotFound({'error' : '{} is not a valid keg id'.format(id)})

    def put(self, id):
        try:
            value = ike_instance._kegManager.dispatch(id, 'get_state')
            value.update(flask.request.get_json())
            form = KegForm.from_json(value)
            if form.validate():
                ike_instance._kegManager.dispatch(id, 'set_state', form.data)
                ret = ike_instance._kegManager.dispatch(id, 'get_state')
            else:
                raise werkzeug.exceptions.BadRequest(form.errors)
        except KeyError:
            raise werkzeug.exceptions.NotFound({'error' : '{} is not a valid keg id'.format(id)})
        return flask.jsonify(ret)

class ThermostatApi(flask.views.MethodView):
    def get(self):
        return flask.jsonify(ike_instance._thermostat.get_state())

    def put(self):
        value = ike_instance._thermostat.get_state()
        value.update(flask.request.get_json())
        form = ThermostatForm.from_json(value)
        if form.validate():
            ike_instance._thermostat.set_state(form.data)
            ret = ike_instance._thermostat.get_state()
        else:
            raise werkzeug.exceptions.BadRequest(form.errors)
        return flask.jsonify(ret)

class KegeratorSettingsApi(flask.views.MethodView):
    def __init__(self):
        super(KegeratorSettingsApi, self).__init__()
        self.db = tinydb.TinyDB(os.path.join(config.DB_ROOT, 'kegerator.json'))
        self.form_validator = KegeratorForm
        if len(self.db.all()) == 0:
            initial = {'name':'Ike',
                       'kegIds': [0, 1]
                       }
            form = self.form_validator.from_json(initial)
            if form.validate():
                self.db.insert(form.data)
            else:
                raise ValueError(form.errors)
    def get(self):
        # return kegerator settings data
        return flask.jsonify(self.db.all()[0])

    def put(self):
        # update ike.thermostat
        value = self.db.all()[0]
        value.update(flask.request.get_json())
        form = self.form_validator.from_json(value)
        if form.validate():
            self.db.update(form.data, eids=[1])
            updated = self.db.all()[0]
            return flask.jsonify(updated)
        else:
            raise werkzeug.exceptions.BadRequest(form.errors)

class SensorsApi(flask.views.MethodView):
    def get(self):
        # return kegerator sensor data
        latest_sensors = ike_instance._logger.find_events(ike.lager.Event.sensors, 'now')
        return flask.jsonify(latest_sensors)

class EventApi(flask.views.MethodView):
    def get(self):
        types = flask.request.args.get('types')
        start = flask.request.args.get('startTime')
        end = flask.request.args.get('endTime')
        # return matching event data
        events = ike_instance._logger.find_events(types, start, end)
        for e in events:
            e.update({'id':e.eid})
        return flask.jsonify(events)

def register_api(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

def launch(_ike_instance):
    global ike_instance
    ike_instance = _ike_instance;
    wtforms_json.init()
    
    api_url_prefix = '/api/v1'

    app = flask.Flask('ike', static_folder=config.STATIC_FILES)

    # beer
    register_api(app, BeerApi, 'beers', api_url_prefix + '/beers/', pk='id')
    
    # users
    register_api(app, UserApi, 'users', api_url_prefix + '/users/', pk='id')

    # keg
    view_func = KegApi.as_view('kegs')
    app.add_url_rule(api_url_prefix + '/kegs/', defaults={'id': None}, view_func=view_func, methods=['GET',])
    app.add_url_rule(api_url_prefix + '%s<%s:%s>' % ('/kegs/', 'int', 'id'), view_func=view_func, methods=['GET', 'PUT'])
    
    # sensors
    app.add_url_rule(api_url_prefix + '/sensors/', view_func=SensorsApi.as_view('sensors'), methods=['GET'])
    app.add_url_rule(api_url_prefix + '/thermostat/', view_func=ThermostatApi.as_view('thermostat'), methods=['GET','PUT'])
    
    # kegerator "core" (whateverthefuck that means)
    app.add_url_rule(api_url_prefix + '/kegerator/', view_func=KegeratorSettingsApi.as_view('kegerator'), methods=['GET','PUT'])
    app.add_url_rule(api_url_prefix + '/events/', view_func=EventApi.as_view('events'), methods=['GET'])
    
    # serve the frontend
    app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
    app.add_url_rule('/<path:path>', 'send_static', lambda path: app.send_static_file(path))

    app.run(host='0.0.0.0', debug=True)
