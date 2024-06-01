from rest_framework import serializers
from ..models.Order import OrderPlataformRelated

class OrderPlataformRelatedSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderPlataformRelated
        exclude = ['order_plataform_id', 'date_published', 'date_updated']


