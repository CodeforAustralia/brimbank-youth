# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0008_auto_20171204_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
