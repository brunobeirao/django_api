# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Call(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    record_start = models.DateTimeField('RECORD_START')
    record_stop = models.DateTimeField('RECORD_STOP')
    source = models.BigIntegerField('SOURCE')
    destination = models.BigIntegerField('DESTINATION')
    duration = models.CharField('DURATION', max_length=10)

    class Meta:
        db_table = 'Call'


class Bill(models.Model):
    id = models.AutoField('ID', primary_key=True)
    price = models.FloatField('PRICE')
    call = models.OneToOneField(Call, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = 'Bill'


class Charge(models.Model):
    id = models.AutoField('ID', primary_key=True)
    standing_charge = models.FloatField('STANDING_CHARGE', max_length=9)
    call_charge = models.FloatField('CALL_CHARGE')
    hour_start = models.IntegerField('STANDARD_START')
    hour_stop = models.IntegerField('STANDARD_STOP')
    active = models.BooleanField('ACTIVE')
    create_date = models.DateField('CREATE_DATE', auto_now_add=True)

    class Meta:
        db_table = 'Charge'
        unique_together = ('standing_charge', 'call_charge')
