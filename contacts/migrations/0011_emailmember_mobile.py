# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-15 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_emailgroup_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmember',
            name='mobile',
            field=models.CharField(max_length=10, null=True),
        ),
    ]