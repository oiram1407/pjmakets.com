from rest_framework import serializers
from ..models.Api import ApiLog

class ApiLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApiLog
        exclude = ['date_published', 'date_updated']


