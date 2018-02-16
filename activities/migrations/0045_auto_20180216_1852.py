# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-16 07:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0044_auto_20180216_1249'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='activity',
            index_together=set([('name', 'activity_type', 'location', 'suburb', 'postcode', 'created_by')]),
        ),
    ]
