## Information
Application that receives call detail records and calculates monthly bills for a given telephone number.

## Project
Django 1.11.21.

Deployed on Heroku.

#### API

    get /api/v1/calls/call/{call_id} 

    get /api/v1/calls/charge 

    post /api/v1/calls/charge 

    post /api/v1/calls/process 

#### Api on Heroku 
https://django-api-call.herokuapp.com/api/v1/calls

#### Swagger
https://django-api-call.herokuapp.com/docs

### Run First time
Data load and process run in project root diretory:

#### Set Charges

    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'https://django-api-call.herokuapp.com/api/v1/calls/charge' --data @charges.json

If you have a saved charge, the actived charge have a status = 1. When you post a new charge, the last posted is status = 0 and the new is status = 1.

You can get:

    https://django-api-call.herokuapp.com/api/v1/calls/charge
    
Returns:

    [
      {
        "id": 1,
        "standing_charge": 0.36,
        "call_charge": 0.09,
        "useful_day": 16,
        "status": 1
      }
    ]
        

#### Process Calls

Post a new json data with call information:

    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'https://django-api-call.herokuapp.com/api/v1/calls/process' --data @data.json
    
data.json example:

    [
      {
        "call_id": 70,
        "start": {
          "type": "start",
          "record_timestamp": "2016-02-29T12:00:00Z",
          "source": 99988526423,
          "destination": 9933468278
        },
        "stop": {
          "type": "stop",
          "record_timestamp": "2016-02-29T14:00:00Z"
        }
      }
    ]

Swagger docs shows the url and is possible to get and post values.

#### Example:

  Get:
    
    https://django-api-call.herokuapp.com/api/v1/calls/77

  Returns:

    [
      {
        "id": 77,
        "record_start": "2018-02-28T21:57:13Z",
        "record_stop": "2018-03-01T22:10:56Z",
        "source": 99988526423,
        "destination": 9933468278,
        "callbills": {
          "id": 8,
          "price": 87,
          "duration": "24:13:43"
        }
      }
    ]
