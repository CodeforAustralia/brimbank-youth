# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0029_activitydraft_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitydraft',
            name='published_ready',
            field=models.BooleanField(default=False),
        ),
    ]