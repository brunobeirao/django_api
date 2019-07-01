# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

id = models.AutoField('ID', primary_key=True)
record_type = models.IntegerField('TYPE', max_length=1)
record_timestamp=models.DateTimeField('RECORD_TIMESTAMP', auto_now_add=True)
call_id=models.IntegerField('CALL_IDENTIFIER')
source=models.IntegerField('SOURCE', max_length=9)
destination=models.IntegerField('DESTINATION', max_length=9)

