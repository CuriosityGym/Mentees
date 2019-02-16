# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-23 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='category',
            field=models.CharField(choices=[('sports', 'SPORTS'), ('current affairs', 'CURRENT AFFAIRS')], default='current affairs', max_length=50),
        ),
    ]