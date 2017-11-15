from rest_framework import serializers
from location.models import Location


class LocationSerializer(serializers.ModelSerializer):
	# Default coordinate
	coordinate = serializers.SerializerMethodField("get_coordinate_data")

	def get_coordinate_data(self, location):
		return {
			"srid": location.coordinate.srid,
			"latitude": location.coordinate.x,
			"longitude": location.coordinate.y
		}

	class Meta:
		model = Location
		fields = "__all__"
