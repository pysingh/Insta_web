# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Insta_Web', '0010_remove_instagramtargetdatabase_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramtargetdatabase',
            name='target',
            field=models.CharField(default='None', max_length=128),
        ),
    ]
