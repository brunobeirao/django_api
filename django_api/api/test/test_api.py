import os
import json
from pathlib import Path
from django.test import TestCase

from django_api.api.models import Charges
from rest_framework import status

BASEDIR = Path(__file__).parents[2]
RESOURCE_DIR = os.path.join(BASEDIR, 'resources')
# settings.configure(default_settings=django_settings)
# settings.configure()


class TestRequests(TestCase):

    def setUp(self):
        self.url_charge = '/api/v1/calls/charge'
        self.charge_dict = {
            'standing_charge': 0.9,
            'call_charge': 0.3,
            'useful_day': 16,
            'status': 1
        }
        charge = Charges(**self.charge_dict)
        charge.save()

        self.datas = {'data': {
            'call_id': 345,
            'start': {
                'type': 'start',
                'record_timestamp': '2017-12-13T03:57:13',
                'source': 999885264,
                'destination': 99334688
            },
            'stop': {
                'type': 'stop',
                'record_timestamp': '2017-12-14T20:10:56'
            }
        }}

    def test_post_process(self):
        self.url = '/api/v1/calls/process'
        json_to_open = 'test.json'
        with open(os.path.join(RESOURCE_DIR, json_to_open)) as json_file:
            data = json.load(json_file)
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.data, data[7])

    def test_get_charges(self):
        response = self.client.get(self.url_charge)
        self.assertEqual(response.data[0]['status'], self.charge_dict['status'])
