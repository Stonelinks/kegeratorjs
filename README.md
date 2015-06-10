# kegeratorjs
Javascript kegerator

TODO: 

```
  /**
   * Scales the value to a [-1, 1] range given the min/max/center
   */
  normalizeInput: function(value, min, max, center) {
    var scaled = 0;

    if(value < center) {
      scaled = -1 * (value - min) / (center - min);
    } else {
      scaled = (value - center) / (max - center);
    }

    if(isNaN(scaled)) {
      scaled = 0;
    }

    return scaled;
  },
  /**
   * Scales the value assuming an input range of [-1, 1]
   */
  scaleOutput: function(value, min, max, center) {
    var scaled = 0;

    if (value > 0) {
      scaled = Math.floor(value * (max - center) + center);
    } else {
      scaled = Math.floor(value * (center - min) + center);
    }

    return scaled;
  }

```
##MODELS##

###kegerator model###
  - beers [ array of beer Ids ]
  - kegs [ array of keg Ids ]
  - events [ array of event Ids ]
  - currentTemperature
  - averageTemperature
  - desiredTemperature (frontend to change this with a PUT)
  - currentKegPressure
  - averageKegPressure
  - currentTankPressure
  - averageTankPressure

###beer model (from web.py)###
  - id (PK)
  - name
  - description
  - picture (optional.. lets do this later)
  - brewedBy
  - style
  - ABV (optional)
  - rating (have a rateBeer(beerId, rating) endpoint in the API somewhere)
  - cost / brew (optional)
  - IBU (bitterness, optional)
  - SRM (color, optional)

###keg model (from web.py)###
  - id (PK)... can just be index in 
  - beerId (maps to a beer model)
  - pintsConsumed
  - pintsTotal
  
###event model (from web.py)###
  - id (PK)
  - timestamp
  - type
    - newKeg: new event on tap
    - pour: someone poured a beer
    - finishedKeg: a keg is dead
    - newUser: added a new user (coming in 1.0)
    - sensorSnapshot: current sensor state
    - settingsSnapshot: current kegerator settings
  - data (arbitrary json string useful for the particular event)
  
###user model (not yet, coming in 1.0)###
  - id
  - name
  - email
  - RFIDTag
  - NFCId
  - untapped account

##VIEWS##

###beer info###
  
  - small display of pertinent beer info
  - have an "advanced" button, maybe pops up a modal?
  
###beer list###

  - just a list of beer info's for all beer in system

###kegerator status widget###

  - temperature and pressure indicators, gauges
  - temperature and pressure stripcharts
  - ability to add / remove an indicator, gauge or stripchart... store this in localstorage
  - list of keg status widgets per keg

###thermosthat stripchart###
  - switch between average and actual
  shows desiredTemperature and currentTemperature are over time
  relay status (on or off)

###keg pressure stripchart###
  shows currentTankPressure over time

###keg consumption stripchart###
  shows plot of beer over time

###keg status widget###
  beer info for current beer
  progress bar of fullness?

###event log (history)###
  - start date
  - end date
  - filteredType
  - list of event log entries
  
###event log entry###
  - will vary depending on type... a table row maybe?

##ENDPOINTS##

###kegerator###

GET /v1/kegerator
  return json serialzation of kegerator model

PUT /v1/kegerator
  update kegerator settings, in this case only desiredTemperature
  return
    json serialzation of kegerator model
  parameters
    desiredTemperature

###beer###

GET /v1/beers
  return all beers in beer db
  parameters
    limit (optional, default to 100)

POST /v1/beers
  create a new beer
  parameters
    whatever fields the beer model needs
  server should create Id, add to beer DB
  return full json of beer

GET /v1/beers/<beerId>
  get info about beer at <beerId>
  return full json of beer 

PUT /v1/beers/<beerId>
  edit beer at <beerId>
  parameters
    whatever fields that need updating
  return full json of beer 

DELETE /v1/beers/<beerId>
  delete beer at <beerId>
  return empty json

###kegs###

GET /v1/kegs
  return all kegs in keg db
  
POST /v1/kegs
  create a new keg
  parameters
    whatever fields the keg model needs
  server should create Id, add to keg DB
  return full json of keg

GET /v1/kegs/<kegId>
  get info about keg at <kegId>
  return full json of keg 

PUT /v1/kegs/<kegId>
  edit keg at <kegId>
  parameters
    whatever fields that need updating
  return full json of keg 

DELETE /v1/kegs/<kegId>
  delete keg at <kegId>
  return empty json

###events###

GET /events
  return
    all events
  parameters
    startDate (if 'now' then just return the last one that matches)
    endDate (optional)
    limit (optional, but default to 100 or something)

GET /events/query
  return
    fields from events of matching types
  parameters
    types [ array of event types ]
    fieldNames [ whatever data you want out of the "data" field for matching event types ]
    startDate (if 'now' then just return the last one that matches)
    endDate (optional)
