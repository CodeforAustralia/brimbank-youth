# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0025_auto_20171215_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitydraft',
            name='space_choice',
            field=models.CharField(blank=True, choices=[('Limited', 'Limited'), ('Unlimited', 'Unlimited')], default='Limited', max_length=50),
        ),
        migrations.AlterField(
            model_name='activitydraft',
            name='space',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
