# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-01 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_recharged'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_recharged',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
