# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 14:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_sensorregistration'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SensorRegistration',
            new_name='SensorData',
        ),
    ]
