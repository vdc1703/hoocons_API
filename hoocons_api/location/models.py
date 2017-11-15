from django.contrib.gis.db import models

# from setting, in CACHES
from caching.base import CachingMixin
from django.contrib.gis.geos import Point

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


"""Inherit from this class to get caching and invalidation helpers."""
@python_2_unicode_compatible
class Location(CachingMixin, models.Model):
    location_name = models.CharField(max_length=250, blank=True, null=True)
    coordinate = models.PointField(default=Point(-181, -91, srid=4326))
    address = models.CharField(max_length=500, blank=True, null=True)
    place_id = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    place_api_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "location"