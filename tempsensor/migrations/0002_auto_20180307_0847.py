# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2018-03-07 00:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempsensor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='column',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='row',
            field=models.IntegerField(default=-1),
        ),
    ]
