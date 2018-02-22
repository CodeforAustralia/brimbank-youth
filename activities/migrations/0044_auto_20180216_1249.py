# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-16 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0043_auto_20180213_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, choices=[('Sport', 'Sport'), ('Learn', 'Learn'), ('School holidays', 'School holidays'), ('Career', 'Career'), ('Culture', 'Art & Culture')], db_index=True, default='Sport', max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.CharField(blank=True, db_index=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(db_index=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='activity',
            name='postcode',
            field=models.CharField(blank=True, db_index=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='suburb',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterIndexTogether(
            name='activity',
            index_together=set([('name', 'activity_type', 'location', 'suburb', 'postcode')]),
        ),
    ]