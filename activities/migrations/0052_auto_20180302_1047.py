# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-03-01 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0051_auto_20180302_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Only females'), ('M', 'Only males'), ('B', 'Both')], default='B', max_length=50),
        ),
        migrations.AlterField(
            model_name='activity',
            name='living_duration',
            field=models.CharField(blank=True, choices=[('Less', 'Less than 5 years'), ('More', 'More than 5 years'), ('Open', 'Open')], default='Open', max_length=50),
        ),
        migrations.AlterField(
            model_name='activitydraft',
            name='gender',
            field=models.CharField(choices=[('F', 'Only females'), ('M', 'Only males'), ('B', 'Both')], default='B', max_length=50),
        ),
        migrations.AlterField(
            model_name='activitydraft',
            name='living_duration',
            field=models.CharField(choices=[('Less', 'Less than 5 years'), ('More', 'More than 5 years'), ('Open', 'Open')], default='Open', max_length=50),
        ),
    ]