# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-28 04:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180116_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
