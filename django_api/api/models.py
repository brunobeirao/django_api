# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Call(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    record_start = models.DateTimeField('RECORD_START')
    record_stop = models.DateTimeField('RECORD_STOP')
    source = models.IntegerField('SOURCE', max_length=9)
    destination = models.IntegerField('DESTINATION', max_length=9)

    class Meta:
        db_table = 'Calls'


class CallBills(models.Model):
    id = models.AutoField('ID', primary_key=True)
    price = models.IntegerField('PRICE', max_length=9)
    call_start_date = models.DateField('CALL_DATE')
    call_start_time = models.TimeField('CALL_TIME')
    duration = models.TimeField('DURATION')
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = 'Bills'
