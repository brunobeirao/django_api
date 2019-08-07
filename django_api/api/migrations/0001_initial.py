# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-04 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('record_start', models.DateTimeField(verbose_name='RECORD_START')),
                ('record_stop', models.DateTimeField(verbose_name='RECORD_STOP')),
                ('source', models.IntegerField(max_length=9, verbose_name='SOURCE')),
                ('destination', models.IntegerField(max_length=9, verbose_name='DESTINATION')),
            ],
            options={
                'db_table': 'Calls',
            },
        ),
        migrations.CreateModel(
            name='CallBills',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(max_length=9, verbose_name='PRICE')),
                ('call_start_date', models.DateField(verbose_name='CALL_DATE')),
                ('call_start_time', models.TimeField(verbose_name='CALL_TIME')),
                ('duration', models.TimeField(verbose_name='DURATION')),
                ('call', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Call')),
            ],
            options={
                'db_table': 'Bills',
            },
        ),
    ]
