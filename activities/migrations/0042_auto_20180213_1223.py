# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-13 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0041_auto_20180207_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitydraft',
            name='postcode',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='activitydraft',
            name='suburb',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('Sport', 'Sport'), ('Learn', 'Learn'), ('School holidays', 'School holidays'), ('Career', 'Career'), ('Culture', 'Art & Culture')], default='Sport', max_length=100),
        ),
        migrations.AlterField(
            model_name='activitydraft',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('Sport', 'Sport'), ('Learn', 'Learn'), ('School holidays', 'School holidays'), ('Career', 'Career'), ('Culture', 'Art & Culture')], default='Sports', max_length=100),
        ),
    ]