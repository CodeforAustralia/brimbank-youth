# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-12-31 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsmember',
            name='mobile',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='smsmember',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]