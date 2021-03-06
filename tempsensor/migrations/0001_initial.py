# -*- coding: utf-8 -*-
# Generated by Django 1.10b1 on 2018-03-14 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorKks', models.CharField(default='', max_length=10)),
                ('x', models.FloatField(default=-1.0, max_length=6)),
                ('y', models.FloatField(default=-1.0, max_length=6)),
                ('row', models.IntegerField(default=-1)),
                ('column', models.IntegerField(default=-1)),
            ],
            options={
                'ordering': ('sensorKks',),
            },
        ),
        migrations.CreateModel(
            name='TempValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default=0, max_length=6)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('sensorKks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempsensor.Sensor')),
            ],
            options={
                'ordering': ('time',),
            },
        ),
    ]
