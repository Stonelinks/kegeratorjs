#kegeratorjs#
[![Build Status](https://travis-ci.org/Stonelinks/kegeratorjs.svg?branch=master)](https://travis-ci.org/Stonelinks/kegeratorjs)

A web enabled kegerator powered by a Javascript front end and Python (Flask) backend

##Getting Started##
  - Customize info about your remot host using the ```environment``` file
  - To resolve dependencies run ```./dependencies``` on the target
  - Deploy to remote host using ```./deploy```
  - Manage server on remote host using ```./start``` ```./stop``` and ```./restart```
  - To copy your public key to the remote host so you don't have to type a password you can run ```./copyKey``` 

###Running without hardware###
  - mocks are used when the host name is not "ike" 
  - To run tests locally use ```./unitTest``` (be sure to resolve dependencies first)
  - To run the server locally with mocked HW support, run ```./src/server/main.py```
 

##MODELS##

###kegerator model###
  - kegs [ array of keg Ids ]
  - name

###thermostat model###
  - degC (read only)
  - avgDegC (read only)
  - compressorOn (read only)
  - deadBandDegC
  - setPointDegC
  - onAddsHeat

###beer model (from api.py)###
  - id (PK)
  - name
  - description
  - picture (coming in 1.0)
  - brewedBy
  - style
  - abv (optional)
  - rating (have a rateBeer(beerId, rating) endpoint in the API somewhere)
  - costPerPint (optional)
  - ibu (bitterness, optional)
  - srm (color, optional)

###keg model (from api.py)###
  - id (PK)... can just be index in 
  - beerId (maps to a beer model)
  - capacityL
  - consumedL
  - flowRateLitersPerSec
  
###event model (from api.py)###
  - id (PK)
  - timestamp
  - type
    - newKeg: new keg on tap
    - pour: someone poured a beer
    - finishedKeg: a keg is dead
    - newUser: added a new user (coming in 1.0)
    - thermostatSense: current thermostat sensed value chaged
    - thermostatSettings: current thermostat settings changed
  - data (arbitrary json string useful for the particular event)
  
###user model (coming in 1.0)###
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

###thermostat stripchart###
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

###kegerator (/api/v1/kegerator)###

####GET####
  - return
	  - json serialzation of kegerator model

####PUT####
  update kegerator settings
  
  - return
	  - json serialzation of kegerator model

###beer (/api/v1/beers/)###

####GET####
  - return all beers in beer db
  - parameters
  - limit (optional, default to 100) (coming in 1.0)

####POST####
  create a new beer, creating new Id, add to beer DB
  
  - parameters
     - whatever fields the beer model needs
  - return ID of new beer

####GET \<beerId\>####
  get info about beer at \<beerId\>
  
  - return full json of beer 

####PUT \<beerId\>####

  edit beer at \<beerId\>
  
  - parameters
    - whatever fields that need updating
  - return
  	 - full json of updated beer model

####DELETE \<beerId\>####
  delete beer at \<beerId\>
  
  - return
	  - empty json

###kegs (/api/v1/kegs/)###

####GET####
  - return all kegs in keg db

####GET \<kegId\>####
  get info about keg at \<kegId\>
  
  - return
	  - full json of keg 

####PUT \<kegId\>####
  edit keg at \<kegId\>
  
  - parameters
	  - whatever fields that need updating
  - return full json of updated keg 

###events (/api/v1/events)###

####GET####

  - return
	  - events of matching specified parameters (or all events)
  - parameters
	  - startDate (if 'now' then just return the last one that matches)
	  - limit (optional, but default to 100 or something) (coming in 1.0)
	  - types [ comma separated list of event types ]
	  - startDate (if 'now' then just return the last one that matches)
	  - endDate (optional)

##Rasbery Pi Setup##
This section is incomplete, but describes steps taken hardware up and running
###ADC Setup (ADS1x15)
This comes mostly from [here](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/io-pins-raspbian/i2c-pins)

Edit the modules file

```sudo nano /etc/modules```

Add these lines:

```
i2c-bcm2708
i2c-dev
```

```sudo apt-get install python-smbus i2c-tools```


##Legal##
This project utilizes Adafruit_I2C.py and Adafruit_ADS1x15.py Copyright (c) 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.