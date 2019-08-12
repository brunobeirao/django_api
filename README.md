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

#### Process Calls

    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'https://django-api-call.herokuapp.com/api/v1/calls/process' --data @data.json

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
