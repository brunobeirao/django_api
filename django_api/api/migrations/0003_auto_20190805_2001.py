# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-05 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190805_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbills',
            name='duration',
            field=models.CharField(max_length=10, verbose_name='DURATION'),
        ),
    ]
