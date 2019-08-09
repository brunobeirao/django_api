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
    duration = models.CharField('DURATION', max_length=10)
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = 'Bills'


class Charges(models.Model):
    id = models.AutoField('ID', primary_key=True)
    standing_charge = models.FloatField('STANDING_CHARGE', max_length=9)
    call_charge = models.FloatField('CALL_CHARGE')
    useful_day = models.IntegerField('USEFUL_DAY')
    status = models.IntegerField('STATUS')
    create_date = models.DateField('CREATE_DATE')

    class Meta:
        db_table = 'Charges'
