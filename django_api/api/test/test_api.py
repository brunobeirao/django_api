import os
import json
from pathlib import Path

from django.test import TestCase
from django_api.api.models import Charges

BASEDIR = Path(__file__).parents[2]
RESOURCE_DIR = os.path.join(BASEDIR, 'resources')


class TestRequests(TestCase):

    def setUp(self):
        self.url_process = '/api/v1/calls/process'
        self.url_call = '/api/v1/calls/call/'
        self.url_charge = '/api/v1/calls/charge'
        self.json_to_open = 'test.json'
        self.charge = {
            'standing_charge': 0.36,
            'call_charge': 0.09,
            'useful_day': 16,
            'status': 1
        }
        charge = Charges(**self.charge)
        charge.save()

    def test_post_process(self):
        with open(os.path.join(RESOURCE_DIR, self.json_to_open)) as json_file:
            data = json.load(json_file)
            response = self.client.post(self.url_process, json.dumps(data), content_type='application/json')
            self.assertEqual(response.data, data[7])

    def test_get_call(self):
        with open(os.path.join(RESOURCE_DIR, self.json_to_open)) as json_file:
            data = json.load(json_file)
            response = self.client.post(self.url_process, json.dumps(data), content_type='application/json')
        call_id = response.data['call_id']
        response = self.client.get(self.url_call + str(call_id))
        self.assertEqual(response.data[0]['id'], call_id)

    def test_get_charges(self):
        response = self.client.get(self.url_charge)
        self.assertEqual(response.data[0]['status'], self.charge['status'])

    def test_post_charges(self):
        response = self.client.post(self.url_charge, json.dumps(self.charge), content_type='application/json')
        self.assertEqual(response.data['status'], self.charge['status'])
