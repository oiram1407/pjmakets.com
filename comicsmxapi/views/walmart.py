from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from ..serializers.api import ApiLogSerializers
from ..generals import Generals as cfg
from ..helpers.plataforms import WalmartHelper, WooCommerceHelper, MercadoLibreHelper
from ..helpers.product import ProductHelper
import json

class WalmartWebhook(APIView):
    def __init__(self):
        self._current_plataform = 'walmart'

    def get(self, request):
        headers = request.headers
        data = request.data
        origin = request.get_host() if(request.get_host() is None) else request.META['REMOTE_ADDR']

        log_api_data = {}
        log_api_data['origin'] = origin
        log_api_data['url'] = request.get_full_path()
        log_api_data['method'] = request.method
        log_api_data['headers'] = json.dumps(dict(headers))
        log_api_data['body'] = json.dumps(dict(request.query_params))

        #CustomerSerializer
        apilog_serializer = ApiLogSerializers(data=log_api_data)
        
        if(apilog_serializer.is_valid()):
            serializer = apilog_serializer.save()

            return Response(apilog_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(apilog_serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        #Check headers
        headers = request.headers
        data = request.data
        status_return = status.HTTP_200_OK
        data_return = {}
        origin = request.get_host() if(request.get_host() is None) else request.META['REMOTE_ADDR']
 
        log_api_data = {}
        log_api_data['origin'] = origin
        log_api_data['url'] = request.get_full_path()
        log_api_data['method'] = request.method
        log_api_data['headers'] = json.dumps(dict(headers))
        log_api_data['body'] = json.dumps(dict(request.data))

        #CustomerSerializer
        apilog_serializer = ApiLogSerializers(data=log_api_data)
        
        if(apilog_serializer.is_valid()):
            apilog_serializer.save()
            pass
        else:
            return Response(apilog_serializer.errors, status=status.HTTP_404_NOT_FOUND)

        type_event = data['type_event']

        walmart_obj = WalmartHelper(1)

        if type_event == 'orders':
            order_data = {} 
        elif type_event == 'products':
            check_item = walmart_obj.findItemBySKU(data['sku'])

            if(check_item is None):  #Create the product
                pass
            else: #Only return
                data_return['status'] = "success"
                data_return['msg'] = "An item already exists with that SKU in Walmart with the ID: "+check_item['wpid']
        
        elif type_event == 'update_inventory':
            _sku = data['sku']
            walmart_product = walmart_obj.findItemBySKU(_sku)
            _walmart_id = walmart_product['wpid']

            obj_product = ProductHelper(_sku)
            walmart_product = obj_product.getProductByRelatedID(_walmart_id, 'walmart')
            
            if(walmart_product is None):
                data_return['msg'] = "Product doesn't exists"

        return Response(data_return, status=status_return)
