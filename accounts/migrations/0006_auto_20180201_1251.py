# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-01 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180128_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_limit',
            field=models.PositiveSmallIntegerField(default=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='sms_limit',
            field=models.PositiveSmallIntegerField(default=20),
        ),
    ]
