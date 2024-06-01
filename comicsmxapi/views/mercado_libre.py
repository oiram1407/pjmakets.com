from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from ..serializers.order import OrderPlataformRelatedSerializers
from ..generals import Generals as cfg
from ..helpers.plataforms import woocommerce
from ..models.Companies import Companie, CompaniesUserRelated, CompaniesPlataformsRelated
from ..models.Order import OrderPlataformRelated
from ..helpers import ProductHelper, InventoryHelper
from ..helpers.plataforms import WooCommerceHelper
import requests
import json

class MecadoLibreSyncView(APIView):
    def __init__(self):
        self._current_plataform = 'mercado_libre'

    def post(self, request):
        user = User.objects.filter(id=request.data['user_id']).first()

        ##Geting relatd company
        company_user = CompaniesUserRelated.objects.filter(user=user).first()

        company = Companie.objects.filter(id=company_user['company']).first()
        #Check if exists prev related
        related = CompaniesPlataformsRelated.objects.filter(company=company).filter(platafom=self._current_plataform).filter(status="Active").first()

        if(related):
            api_meli = cfg.getSettingParammeter('meli_api_url')
            url = api_meli+"/oauth/token"

            payload = 'grant_type=client_credentials&client_id=2979946054061752&client_secret=6xCbqn3PY9FWqZfu2wsbIcMl34AiMBQb'
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            return Response(response, status=status.HTTP_200_OK)
        else:
            pass

class MercadoLibreAccount:

    def __init__(self, data):
        self._current_plataform = 'mercado_libre'
        self.grant_type = data['grant_type']
        self.client_id = data['client_id']
        self.client_secret = data['client_secret']
        self._order_id = data['order_id']

    def getToken(self):
        api_meli = cfg.getSettingParammeter('meli_api_url')
        url = api_meli+"/oauth/token"

        payload = 'grant_type='+self.grant_type+'&client_id='+self.client_id+'&client_secret='+self.client_secret
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        self._access_token = response['access_token']

        return self._access_token
    
    def getOrderData(self, company, user):
        self.getToken()

        api_meli = cfg.getSettingParammeter('meli_api_url')
        url = api_meli+"/orders/"+self._order_id

        headers = {
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("GET", url, headers=headers)
        order_data = response.json()
        _order_items = order_data['order_items']
        items = {}
        item_count = 0
        
        for i in range(len(_order_items)):
            items[item_count] = {
                "sku": _order_items[i]['item']['seller_sku'],
                "quantity": _order_items[i]['quantity'],
                "full_unit_price": _order_items[i]['full_unit_price'],
                "sale_fee": _order_items[i]['sale_fee'],
            }

            item_count+=1

        response_order_data = {
            "order_plataform_id": str(order_data['id']),
            "plataform": self._current_plataform,
            "total_amount": order_data['total_amount'],
            "paid_amount": order_data['paid_amount'],
            "date_order": order_data['date_created'],
            "buyer_id": order_data['buyer']['id'],
            "buyer_first_name": order_data['buyer']['first_name'],
            "company": company.id,
            "user": user.id,
            "data": json.dumps(items)
        }

        return response_order_data
    
    def sendMessageOrder(self):
        pass
        
class WebhookMeli(APIView):

    def __init__(self):
        self._current_plataform = 'mercado_libre'

    def checkOrder(self, order_id):
        order = OrderPlataformRelated.objects.filter(order_plataform_id=order_id).first()

        return order
    
    def getUserCompanyRelated(self, app_id):
        app_id = str(app_id)
        company_related_plataform = CompaniesPlataformsRelated.objects.filter(data__contains='"app_id": "'+app_id+'"').filter(plataform=self._current_plataform ).first()

        return company_related_plataform
    
    def getUserCompany(self, company_id):
        company_id = int(company_id)
        company = Companie.objects.filter(id=company_id).first()

        return company
    
    def getUser(self, user_id):
        user = User.objects.filter(id=user_id).first()

        return user
    
    def getProducts(self, data):
        products = json.loads(data)

        return products

    def post(self, request):
        data = request.data
        type_event = data['topic']
        resource = data['resource']
        data_response = {}

        if type_event == 'orders_v2':
            order_data = {}
            order_id_meli = resource.split("/orders/")
            order_id_meli = order_id_meli[1]
            check_order_exists = self.checkOrder(order_id_meli)

            if not check_order_exists:
                company_related = self.getUserCompanyRelated(data['application_id'])
                company = self.getUserCompany(company_related.company_id)
                user = self.getUser(company_related.user_id)
                company_related = json.loads(company_related.data)

                company_info = {
                    "grant_type": "client_credentials",
                    "client_id": company_related['app_id'],
                    "client_secret": company_related['client_secret'],
                    "order_id": order_id_meli
                }
                
                meli_obj = MercadoLibreAccount(company_info)
                meli_order = meli_obj.getOrderData(company, user)
                order_plataform_serializar = OrderPlataformRelatedSerializers(data=meli_order)

                #create order Register in system
                if(order_plataform_serializar.is_valid()): #Errors
                    pass
                else:
                    return Response(order_plataform_serializar.errors, status=status.HTTP_400_BAD_REQUEST)
                
                #Save order
                order_plataform_serializar.save()

                products_list = self.getProducts(meli_order['data'])
                products_list = products_list.values()

                for product in products_list:
                    product_obj_tmp = ProductHelper(product['sku'])
                    product_obj = product_obj_tmp.getProductBySKU()
                    quantity_to_discount = product['quantity']
                    action_type = 'decrement'

                    #Get current inventory
                    inventory_obj = InventoryHelper(product_obj, quantity_to_discount)
                    current_inventory = inventory_obj.getProductInventory()
                    new_inventory = int(current_inventory.quantity) - int(quantity_to_discount)

                    #Creating inventory update increse/decrese quantity
                    inventory_update_data = {
                        "quantity": quantity_to_discount,
                        "method_update": self._current_plataform ,
                        "product": product_obj.id,
                        "user": user.id,
                        "action_type": action_type
                    }

                    inventory_obj.setProductInventoyUpdate(inventory_update_data)
                    
                    #Creating inventoy log
                    updated_log = "The Product Data has been updated successfuly with the next information: Prev. inventory "+str(current_inventory.quantity)+" "+action_type+" "+str(quantity_to_discount)+" pcs, New innventory "+str(new_inventory)
                    
                    update_log_data = {
                        "product": product_obj.id,
                        "method": self._current_plataform,
                        "action": updated_log,
                        "action_type": action_type,
                        "user": user.id,
                    }

                    inventory_obj.setPoductUpdateLog(update_log_data)

                    #Updating current inventory from product
                    product_inventory_data = {
                        "product": product_obj.id,
                        "quantity": new_inventory,
                        "user": user.id
                    }
                
                    inventory_obj.setProductInventory(product_inventory_data)

                    #Call anothers plataforms to compair new inventory
                    woocommerce = WooCommerceHelper()
                    _woocommerce_company = woocommerce.WoocommerAccountByCompany(company)
                    _woocommerce_product = woocommerce.getProductBySKU(product['sku'])
                    _woocommerce_product_related = woocommerce.getProductRelated()
                    _woocommerce_set_inventory = woocommerce.setInventory(new_inventory)

                    if(_woocommerce_set_inventory['id']):
                        order_data['woo_stock'] = "Woocommerces stock for this product has been updated successfully"
                    else:
                        order_data['woo_stock'] = "Woocommerces stock for this product had an error"

                #Update product inventory
                order_data['order_plataform_id'] = order_id_meli
                order_data['plataform'] = self._current_plataform 

                data_response['status'] = 'success'
                data_response['message'] = "Order created succesfully"
                data_response['data'] = order_data
                response_status = status.HTTP_201_CREATED
            else:
                data_response['status'] = 'success'
                data_response['message'] = "Order has been created already"
                data_response['data'] = {}

                response_status = status.HTTP_200_OK

        return Response(data_response, status=response_status)

