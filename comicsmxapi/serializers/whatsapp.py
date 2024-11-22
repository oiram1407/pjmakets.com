from rest_framework import serializers
from ..models.Whatsapp import *

class WaMessagesTemplatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = WaMessagesTemplates  
        exclude = ['date_published', 'date_updated']

class WaOutCommingLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = WaOutCommingLog
        exclude = ['date_published', 'date_updated']

class WaSendMultipleNumberMessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = WaOutcomigProgramedMessages
        exclude = ['date_published', 'date_updated']