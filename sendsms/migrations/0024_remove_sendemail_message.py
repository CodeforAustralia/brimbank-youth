# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-03-01 04:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sendsms', '0023_auto_20180222_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendemail',
            name='message',
        ),
    ]
