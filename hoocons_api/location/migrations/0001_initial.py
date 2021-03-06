# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 15:53
from __future__ import unicode_literals

import caching.base
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(blank=True, max_length=250, null=True)),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(-181, -91, srid=4326), srid=4326)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('place_id', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('place_api_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'location',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
    ]
