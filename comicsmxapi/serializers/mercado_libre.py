from rest_framework import serializers
from ..models.Order import OrderPlataformRelated

class MercadoLibreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPlataformRelated
        exclude = ['date_published', 'date_updated']
    