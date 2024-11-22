from rest_framework import serializers
from ..models.ShipProviders import ShipProviders

class ShipProvidersSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShipProviders
        exclude = ['date_published', 'date_updated']