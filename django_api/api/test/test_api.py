import pytest
import os
import json
from pathlib import Path
import requests_mock
from django.test import TestCase
from django.conf import settings
from rest_framework import status

BASEDIR = Path(__file__).parents[2]
RESOURCE_DIR = os.path.join(BASEDIR, 'resources')
settings.configure()

class TestRequests(TestCase):

    def test_post(self):
        self.url = '/api/v1/calls/process'
        json_to_open = 'test.json'
        with open(os.path.join(RESOURCE_DIR, json_to_open)) as json_file:
            dict_data = json.load(json_file)
            with requests_mock.mock() as mock:
                # mock.post(status_code=status.HTTP_200_OK)
                response = self.client.post(self.url, dict_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
