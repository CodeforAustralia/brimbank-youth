# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-03-02 00:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_organisation_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='organisation_logo',
        ),
    ]
