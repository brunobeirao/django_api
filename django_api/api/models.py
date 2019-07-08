# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Call(models.Model):
    call_id = models.IntegerField('ID', primary_key=True)

    class Meta:
        db_table = 'Calls'


class StartCallRecord(models.Model):
    id = models.AutoField('ID', primary_key=True)
    record_timestamp = models.DateTimeField('RECORD_TIMESTAMP')
    source = models.IntegerField('SOURCE', max_length=9)
    destination = models.IntegerField('DESTINATION', max_length=9)
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = 'Starts'


class StopCallRecord(models.Model):
    id = models.AutoField('ID', primary_key=True)
    record_timestamp = models.DateTimeField('RECORD_TIMESTAMP')
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = 'Stops'


class CallBills(models.Model):
    id = models.AutoField('ID', primary_key=True)
    price = models.IntegerField('PRICE', max_length=9)
    duration = models.DateTimeField('DURATION', auto_now_add=True)
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)