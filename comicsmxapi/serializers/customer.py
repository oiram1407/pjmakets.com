from rest_framework import serializers
from ..models.Customer import Customer, CustomerNotifications

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['date_published', 'date_updated']

class CustomerNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotifications
        exclude = ['date_published', 'date_updated']