# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-01 23:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20180102_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsmember',
            name='group',
        ),
        migrations.AddField(
            model_name='smsmember',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_members', to='contacts.ContactGroup'),
        ),
    ]