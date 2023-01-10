from rest_framework import serializers #serializers import ettik

from .models import Flight #Flight Tablomuzu import ettik.

#Flight kısmına iat serializers
class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )