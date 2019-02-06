# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 18:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20180217_1355'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game_save',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]