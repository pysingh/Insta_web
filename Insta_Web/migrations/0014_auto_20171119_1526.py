# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Insta_Web', '0013_auto_20171119_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramtargetdatabase',
            name='followers_usernameids',
            field=models.CharField(default='0', max_length=256),
        ),
        migrations.AddField(
            model_name='instagramtargetdatabase',
            name='following_mediaids',
            field=models.CharField(default='0', max_length=256),
        ),
    ]
