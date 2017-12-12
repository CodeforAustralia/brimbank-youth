# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 05:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendsms', '0003_auto_20171209_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('message', models.TextField(blank=True, max_length=500)),
            ],
        ),
    ]