from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.whatsapp import WaMessagesTemplatesSerializers, WaOutCommingLogSerializers
from ..models import *
from rest_framework import status
from twilio.rest import Client
from django.contrib.auth.models import User
from ..generals import Generals


# Create your views here.
class WaMessageTemplatesView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        wa_messages_templates = WaMessagesTemplates.objects.all()
        serializer = WaMessagesTemplatesSerializers(wa_messages_templates, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = WaMessagesTemplatesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WaSendMultipleNumberMessageView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        wa_outcomming_message = WaOutCommingLog.objects.all()
        serializer = WaOutCommingLogSerializers(wa_outcomming_message, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        conf_param = Generals
        data = request.data #Getting information to send notification
        template_id = data['template']
        to_number = data['to_number']
        to_number.replace(" ", "")
        prefix_number = conf_param.getSettingParammeter('mexican_phone_prefix')
        media = data['mediaUrl'] if(data['mediaUrl']) else ''

        parameters_in = data['params_sent'] #assign variable to params in request
        parameters = parameters_in.split('|') #separeting all params in dict
        params_quantity = len(parameters) #length from params

        if(len(to_number) < 13): #Completing number with phone prefix
            to_number = prefix_number+to_number


        #Get mesagge from template
        template = WaMessagesTemplates.objects.filter(id=template_id).first()
        message = template.message

        #change params from real information
        for i in range(params_quantity):
            message = message.replace("{"+str(i+1)+"}", parameters[i])

        # Send whatsapp message
        account_sid = conf_param.getSettingParammeter('twilio_account_sid')
        auth_token  = conf_param.getSettingParammeter('twilio_auth_token')
        from_number =conf_param.getSettingParammeter('twilio_phone_number')

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="whatsapp:"+to_number,
            from_="whatsapp:"+from_number,
            body=message,
            #media_url=[media]
            )
        
        res = {
            "status": "failed_to_send",
            "msg": "Message not sent to"+to_number,
            "sid": ""
        }
        
        if(message.sid):
            res = {
                "status": "sent",
                "msg": "Mssage sent to"+to_number,
                "sid": message.sid
            }

        #Guardamos el log del mensaje enviado
        if(res['status'] == "sent"):
            log = {
                "to_number":to_number, 
                "template":template,
                "params_sent":parameters_in, 
                "message_sid":res['sid']
            }

            #Generamos el objeto que se vaalidara en el serializer
            
            serializer = WaOutCommingLog(**log)
            serializer.save()
                
            return Response(res, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    