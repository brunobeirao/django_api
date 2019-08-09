# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-09 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190805_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('standing_charge', models.FloatField(max_length=9, verbose_name='STANDING_CHARGE')),
                ('call_charge', models.FloatField(verbose_name='CALL_CHARGE')),
                ('useful_day', models.IntegerField(verbose_name='USEFUL_DAY')),
                ('status', models.IntegerField(verbose_name='STATUS')),
                ('create_date', models.DateField(verbose_name='CREATE_DATE')),
            ],
            options={
                'db_table': 'Charges',
            },
        ),
    ]