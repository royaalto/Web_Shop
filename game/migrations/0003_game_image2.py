# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-16 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20180213_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=game.models.user_directory_path),
        ),
    ]
