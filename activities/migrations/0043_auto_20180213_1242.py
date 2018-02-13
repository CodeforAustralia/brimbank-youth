# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-13 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0042_auto_20180213_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='postcode',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='suburb',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
