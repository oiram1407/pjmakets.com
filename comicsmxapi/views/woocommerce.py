from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..generals import Generals as cfg
from ..helpers.plataforms import woocommerce, mercado_libre
from ..helpers.product import ProductHelper
from ..helpers.inventory import InventoryHelper
from ..helpers.notifications import NotificationsWhatsapp
from ..helpers.order import Order
from ..helpers.customer import CustomerHelper
from ..models.Companies import Companie
from ..models.Customer import CustomerNotifications 
from ..serializers.order import OrderPlataformRelatedSerializers
from ..serializers.customer import CustomerSerializer, CustomerNotificationsSerializer
from ..serializers.product import ProductSerializer
from ..serializers.api import ApiLogSerializers
import json
import requests
import pendulum
import random
import re

class WoocommerceWebhook(APIView):

    def __init__(self) -> None:
        self._current_plataform = 'woocommerce'

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

    def update(self, request):
        return self.post(request)

    def post(self, request):
        #Check headers
        headers = request.headers
        data = request.data
        origin = request.get_host() if(request.get_host() != None) else request.META['REMOTE_ADDR']

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

        try:
           if(data['webhook_id'] != None):
                return Response({"msg": "ok"}, status=status.HTTP_200_OK)
        except:
            pass

        try:
            if(headers['x-wc-webhook-source'] != None):
                url_store = headers['x-wc-webhook-source']
            if(headers['x-wc-webhook-topic'] != None):
                event = headers['x-wc-webhook-topic']
        except:
            url_store = 'https://comicsmx.com/'
            event = 'product.updated'

        (type_event, action_event) = event.split('.')

        woocommerce_obj = woocommerce.WooCommerceHelper()
        woocommerce_store = woocommerce_obj.WoocommerceAccountByURL(url_store)
        self._platform = 'woocommerce'
        self._company_id = woocommerce_store.company.id
        self._company = Companie.objects.get(pk=self._company_id)
        data_response = {}

        if type_event == 'order':
            self._order_id = self._current_plataform+'_'+str(data['id'])

            data_customer = data['billing']
            data_customer['phone'].replace(" ", "")
            
            customer_data = {}
            customer_data['first_name'] = data_customer['first_name']
            customer_data['last_name'] = data_customer['last_name']
            customer_data['email'] = data_customer['email']
            customer_data['phone'] = data_customer['phone']
            customer_data['company'] = self._company_id
            
            #CustomerSerializer
            customer_serializer = CustomerSerializer(data=customer_data)
            
            if(customer_serializer.is_valid()):
                pass
            else:
                return Response(customer_serializer.errors, status=status.HTTP_404_NOT_FOUND)

            customer_obj = CustomerHelper(customer_data['phone'])
            customer_obj_f = customer_obj.getCustomerID()
            
            if(customer_obj_f is None):
                customer_obj_f = customer_serializer.save()

            #send customer whatsapp notification
            params = ""
            shp_lines = data['shipping_lines'][0]
            params = f"{data['billing']['first_name']}|ComicsMX|#{str(data['id'])}"
            #calc date tiime
            date_paid = pendulum.parse(data['date_paid']) if(data['date_paid']) else ''
            
            atc_num = "5529131454"

            rand_num = random.randrange(2)
            final_rand = {
                0: "y mejores bolsas protectoras para tu coleccion en el siguiente link https://bit.ly/3W2vOYB",
                1: "para tu colección en www.comicsmx.com",
                2: "coleccionables como funko pop en el siguiente link https://bit.ly/3Uwk7XP"
            }
            wa_notiification = NotificationsWhatsapp()

            order_data = {}
            order_data['company'] = self._company_id
            order_data['plataform'] = self._current_plataform
            order_data['order_plataform_id'] = self._order_id
            order_data['total_amount'] = data['total']
            order_data['paid_amount'] = data['total']
            order_data['date_order'] = data['date_created']
            order_data['user'] = self._company.user.id
            order_data['status'] = woocommerce_obj.fixStatus(data['status'])

            _order_items = data['line_items']
            items = {}
            item_count = 0

            for i in range(len(_order_items)):
                items[item_count] = {
                    "sku": _order_items[i]['sku'],
                    "quantity": _order_items[i]['quantity'],
                    "full_unit_price": _order_items[i]['subtotal'],
                    "sale_fee": _order_items[i]['total_tax'],
                }

                item_count+=1

            order_data['data'] = json.dumps(items)

            check_order = woocommerce_obj.checkOrder(self._order_id)

            if(check_order is None):
                order_plataform_serializar = OrderPlataformRelatedSerializers(data=order_data)
                
                #create order Register in system
                if(order_plataform_serializar.is_valid()): #Errors
                    order_related = order_plataform_serializar.save()
                    data_response['status'] = f"The order related was created with ID: {order_related.pk}"
                else:
                    return Response(order_plataform_serializar.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                data_response['order_ralate'] = f"The order related has alrady created with ID: {check_order.pk}"
            
            if action_event == 'created':

                if order_data['status'] == 'paid':
                    
                    if(shp_lines['method_id'] == 'local_pickup'):
                        next_saturday = date_paid.next(pendulum.SATURDAY).format('dddd D [de] MMMM [del] Y', locale='es')
                        delivery_location = "en metro hidalgo"
                        delivery_instruction = "realizamos las entregas a un costado de metro hidalgo frente al subway sobre Av. Paseo de Refrma"
                        delivery_schedule = "12:00pm a 13:00pm"
                        params += f"|{delivery_location}|{delivery_schedule}|{next_saturday}|{delivery_instruction}|{atc_num}|{final_rand[rand_num]}"
                        action = 'delivery_comicsmx_final'

                    elif(shp_lines['method_id'] == 'flat_rate' or shp_lines['method_id'] == 'skydropx-pro'):
                        params += f'|{atc_num}|{final_rand[rand_num]}'
                        action = 'order_confimer_shpmethod'
                    
                    data['billing']['phone'].replace(" ", "")
                    
                    params_notification = {
                        "to_number": f"{data['billing']['phone']}",
                        "params_sent": params,
                        "template": wa_notiification.getIDTemplateByName(action),
                        "mediaUrl": ""
                    }
                    params_notification = json.dumps(params_notification)

                    url_notification = f"{cfg.getSettingParammeter('self_api_url')}{reverse('send-customer-notification')}"

                    headers = {
                        'Content-Type': 'application/json'
                    }
                    
                    send_notification = requests.request("POST", url_notification, headers=headers, data=params_notification)
                    send_notification = send_notification.json()

                    if(send_notification['status'] == 'sent'):
                        notification_log = {
                            "customer": customer_obj_f.id,
                            "template": wa_template_id,
                            "data": params_notification,
                            "status": send_notification['status'],
                            "order": order_plataform_serializar.pk,
                            "type_notification": "order_recived"
                        }

                        notification_log_serializer = CustomerNotificationsSerializer(data=notification_log)

                        if(notification_log_serializer.is_valid()):
                            
                            notification_log_serializer.save()

                    data_response['notification_sent'] = send_notification['status']

                    products_list = json.loads(order_data['data']).values()

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
                            "method_update": self._current_plataform,
                            "product": product_obj.id,
                            "user": self._company.user.id,
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
                            "user": self._company.user.id,
                        }

                        inventory_obj.setPoductUpdateLog(update_log_data)

                        #Updating current inventory from product
                        product_inventory_data = {
                            "product": product_obj.id,
                            "quantity": new_inventory,
                            "user": self._company.user.id,
                        }
                    
                        inventory_obj.setProductInventory(product_inventory_data)

                        #Call anothers plataforms to compair new inventory
                        _mercado_libre = mercado_libre.MercadoLibreHelper(self._company)
                        _mercado_libre_product_id = _mercado_libre.getIDProductBySKU(product['sku'])
                        
                        if(_mercado_libre_product_id is None):
                            data_response['meli_stock'] = 'The product with SKU: '+product['sku']+' does not exists in MELI Account'
                        else:
                            _mercado_libre_product = _mercado_libre.setInventory(product_obj.id)

                            if _mercado_libre_product['id']:
                                data_response['meli_stock'] = 'The stock for product with SKU: '+product['sku']+' has been updated succesfully'
                                data_response['status'] = status.HTTP_200_OK
                            else:
                                data_response['meli_stock'] = 'The stock for product with SKU: '+product['sku']+' had an error'
                                data_response['status'] = status.HTTP_400_BAD_REQUEST
                    
                #declare dic for order information
                data_response['status'] = status.HTTP_201_CREATED
                data_response['message'] = 'Orden has been created successfuly'

            elif action_event == 'updated':
                current_oder_obj = Order(self._order_id)
                current_order = current_oder_obj.getOrderID()
                current_order_new_status = current_oder_obj.setNewOrderStatus(order_data['status'])

                if order_data['status'] == 'paid':

                    if(shp_lines['method_id'] == 'local_pickup'):
                        next_saturday = date_paid.next(pendulum.SATURDAY).format('dddd D [de] MMMM [del] Y', locale='es')
                        delivery_location = "en metro hidalgo"
                        delivery_instruction = "realizamos las entregas a un costado de metro hidalgo frente al subway sobre Av. Paseo de Refrma"
                        delivery_schedule = "12:00pm a 13:00pm"
                        params += f"|{delivery_location}|{delivery_schedule}|{next_saturday}|{delivery_instruction}|{atc_num}|{final_rand[rand_num]}"
                        action = 'delivery_comicsmx_final'

                    elif(shp_lines['method_id'] == 'flat_rate'):
                        params += f'|{atc_num}|{final_rand[rand_num]}'
                        action = 'order_confimer_shpmethod'

                    wa_template_id = wa_notiification.getIDTemplateByName(action)
                    data['billing']['phone'].replace(" ", "")
                    params_notification = {
                        "to_number": f"{data['billing']['phone']}",
                        "params_sent": params,
                        "template": wa_template_id,
                        "mediaUrl": ""
                    }
                    params_notification = json.dumps(params_notification)

                    url_notification = f"{cfg.getSettingParammeter('self_api_url')}{reverse('send-customer-notification')}"
                    
                    headers = {
                        'Content-Type': 'application/json'
                    }

                    send_notification = requests.request("POST", url_notification, headers=headers, data=params_notification)
                    send_notification = send_notification.json()

                    if(send_notification['status'] == 'sent'):
                        notification_log = {
                            "customer": customer_obj_f.id,
                            "template": wa_template_id,
                            "data": params_notification,
                            "status": send_notification['status'],
                            "order": current_order
                        }

                        notification_log_serializer = CustomerNotificationsSerializer(data=notification_log)

                        if(notification_log_serializer.is_valid()):
                            notification_log_serializer.save()

                    data_response['notification_sent'] = send_notification['status']
                        

                    products_list = json.loads(order_data['data']).values()

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
                            "method_update": self._current_plataform,
                            "product": product_obj.id,
                            "user": self._company.user.id,
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
                            "user": self._company.user.id,
                        }

                        inventory_obj.setPoductUpdateLog(update_log_data)

                        #Updating current inventory from product
                        product_inventory_data = {
                            "product": product_obj.id,
                            "quantity": new_inventory,
                            "user": self._company.user.id,
                        }
                    
                        inventory_obj.setProductInventory(product_inventory_data)

                        #Call anothers plataforms to compair new inventory
                        _mercado_libre = mercado_libre.MercadoLibreHelper(self._company)
                        _mercado_libre_product_id = _mercado_libre.getIDProductBySKU(product['sku'])
                        
                        if(_mercado_libre_product_id is None):
                            data_response['meli_stock'] = 'The product with SKU: '+product['sku']+' does not exists in MELI Account'
                        else:
                            _mercado_libre_product = _mercado_libre.setInventory(product_obj.id)
                            
                            if _mercado_libre_product['id']:
                                data_response['meli_stock'] = 'The stock for product with SKU: '+product['sku']+' has been updated succesfully'
                                data_response['status'] = status.HTTP_200_OK
                            else:
                                data_response['meli_stock'] = 'The stock for product with SKU: '+product['sku']+' had an error'
                                data_response['status'] = status.HTTP_400_BAD_REQUEST

                elif order_data['status'] == 'failed':
                    pass

                #declare dic for order information
                data_response['status'] = status.HTTP_200_OK
                data_response['message'] = 'Orden has been updated successfuly'

            else:
                
                data_response['message'] = "An error ocurried while create order"
            
            data_response['status'] = data_response['status'] if(data_response['status']) else status.HTTP_200_OK

            return Response(data_response)
        
        elif type_event == 'product':
            _product_sku = None
            product_sku = data['sku']
            #Initialite helper object
            product_obj = ProductHelper(product_sku)

            #preg description field
            product_description = data['description']
            html_pattern = "\n|\t|<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>"
            product_description = re.sub(html_pattern, '', product_description) 

            #definne params variables
            product_name = data['name']
            product_platform_related = f"{woocommerce_store.company.name}_#{data['id']}"
            product_price = data['regular_price']
            product_status = product_obj.fixProductStatusWoo(data['status'])
            product_stock = data['stock_quantity']
            product_weight = data['weight']
            product_height = data['dimensions']['height']
            product_width = data['dimensions']['width']
            product_length = data['dimensions']['length']
            product_editorial = ''
            product_collection = ''
            product_isbn = ''
            product_author = ''

            for i in range(len(data['attributes'])):
                _attr = data['attributes'][i]

                if _attr['name'].lower() == 'isbn':
                    product_isbn+=_attr['options'][0]

                if _attr['name'].lower() == 'autor':
                    product_author+=_attr['options'][0]

            editorials = (
                "Arechi Manga",
                "Panini Manga", 
                "Panini España",
                "Kamite", 
                "MangaLine", 
                "Planeta Comics", 
                "Planeta Comics España",
                "DC", 
                "Marvel", 
                "Norma", 
                "Ivrea", 
                "Ivrea Argentina",
                "Milky Way Ediciones",
                "ECC",
                "Ediciones La Cupula",
                "Kibook Ediciones",
                "Kodai",
                "Bolsas Resistencia de México",
                "Kemuri Ediciones",
                "Ovni Press",
                "Ponent Mon",
                "Tomodomo",
                "Ediciones Babylon",
                "Distrito Manga"
            )

            _categories = data['categories']

            for i in range(len(_categories)):
                if(_categories[i]['name'] in editorials):
                    product_editorial = _categories[i]['name']
                else:
                    if(_categories[i]['name'] != 'Novedades de la semana'):
                        product_collection = _categories[i]['name']

            _product_images = data['images']
            images = []
            _image_count = 0

            for i in range(len(_product_images)):
                images.append({
                    "source": _product_images[_image_count]['src']
                })

            product_obj_meli = mercado_libre.MercadoLibreHelper(self._company)
            self._product = product_obj.getProductByRelatedID(product_platform_related, self._platform)

            if action_event == 'created':
                
                if (self._product is None):
                    #Saving product in main sistem
                    product_data = {
                        "name": product_name,
                        "sku": product_sku,
                        "status": product_status,
                        "company": self._company.pk,
                        "user": self._company.user.id,
                    }
                    
                    product_serializer = ProductSerializer(data=product_data)
                    
                    if(product_serializer.is_valid()):
                        pass
                    else:
                        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                    self._product = product_serializer.save()

                    _data_product_meta = {
                        "product": self._product.id,
                        "description": product_description,
                        "images": json.dumps(images),
                        "weight": product_weight,
                        "height": product_height,
                        "width": product_width,
                        "length": product_length,
                        "user": self._company.user.id
                    }

                    product_meta = product_obj.setProductMeta(_data_product_meta)
                    
                    _data_product_price = {
                        "product": self._product.id,
                        "plataform_name": self._current_plataform,
                        "product_price": product_price,
                        "user": self._company.user.id
                    }

                    _product_price = product_obj.setProductPrice(_data_product_price)

                    _data_product_inventory = {
                        "method_update": self._platform,
                        "user": self._company.user.id
                    }

                    inventory_obj = InventoryHelper(self._product, product_stock)

                    _product_inventory = inventory_obj.setNewProductInventory(_data_product_inventory)
                    _product_update_inventory = inventory_obj.setProductInventoyUpdate(_data_product_inventory)
                    data_response['id'] = f"The product has been created succesfullly with de the next ID {self._product.id}"

                    check_product_woo = product_obj.getProductRelatedID(self._product.id, self._platform)

                    if(check_product_woo is None):
                        #Save product woo
                        _product_related_woo_data = {
                            "product": self._product.id,
                            "product_plataform_id": product_platform_related,
                            "method": self._platform,
                            "user": self._company.user.id
                        }

                        _woo_product = product_obj.setProductRelated(_product_related_woo_data)
                        data_response['woocommerce'] = f"The product {product_platform_related} has been saved succesfully with the next related product id {_woo_product.id}"
                
                else:
                    data_response['woocommerce'] = f"The product already exists with de the next ID {self._product.id}"

                data_response['status'] = status.HTTP_200_OK

            elif action_event == 'updated':
                if (self._product is None):
                    #Saving product in main system
                    product_data = {
                        "name": product_name,
                        "sku": product_sku,
                        "status": product_status,
                        "company": self._company.pk,
                        "user": self._company.user.id,
                    }
                    
                    product_serializer = ProductSerializer(data=product_data)
                    
                    if(product_serializer.is_valid()):
                        self._product = product_serializer.save()
                    else:
                        self._product = product_obj.getProductBySKU()

                    _data_product_meta = {
                        "product": self._product.id,
                        "description": product_description,
                        "images": json.dumps(images),
                        "weight": product_weight,
                        "height": product_height,
                        "width": product_width,
                        "length": product_length,
                        "user": self._company.user.id
                    }

                    product_meta = product_obj.setProductMeta(_data_product_meta)

                    _data_product_price = {
                        "product": self._product.id,
                        "plataform_name": self._current_plataform,
                        "product_price": product_price,
                        "user": self._company.user.id
                    }

                    _product_price = product_obj.setProductPrice(_data_product_price)
                    check_product_woo = product_obj.getProductRelatedID(self._product.id, self._platform)

                    if(check_product_woo is None):
                        #Save product woo
                        _product_related_woo_data = {
                            "product": self._product.id,
                            "product_plataform_id": product_platform_related,
                            "method": self._platform,
                            "user": self._company.user.id
                        }

                        _product_related_woo = product_obj.setProductRelated(_product_related_woo_data)
                    
                else:
                    _product_sku = self._product.sku

                    #Update prduct iformation
                    #Saving product in main sistem
                    product_data = {
                        "name": product_name,
                        "sku": product_sku,
                        "status": product_status,
                    }
                    
                    product_update = product_obj.updateProductData(self._product.id, product_data)

                    _data_product_meta = {
                        "description": product_description,
                        "images": json.dumps(images),
                        "weight": product_weight,
                        "height": product_height,
                        "width": product_width,
                        "length": product_length,
                    }

                    product_meta = product_obj.updateProductDataMeta(self._product.id, _data_product_meta)
                    
                    _data_product_price = {
                        "plataform_name": self._current_plataform,
                        "product_price": product_price
                    }

                    _product_price = product_obj.updateProductDataPrice(self._product.id, _data_product_price)


                    inventory_obj = InventoryHelper(self._product, product_stock)
                    _inventory_obj_ = inventory_obj.getProductInventory()

                    _data_product_inventory = {
                        "method_update": self._platform,
                        "product": self._product.id,
                        "quantity": product_stock,
                        "user": self._company.user.id,
                        "current_inventory": _inventory_obj_.quantity,
                        "action_type": 'decrement' if(product_stock < _inventory_obj_.quantity) else 'increment'
                    }

                    _product_inventory = inventory_obj.setProductInventory(_data_product_inventory)
                    _product_update_inventory = inventory_obj.setProductInventoyUpdate(_data_product_inventory)
                    data_response['id'] = f"The product has been updated succesfullly with de the next ID {self._product.id}"

                    check_product_woo = product_obj.getProductRelatedID(self._product.id, self._platform)

                    if(check_product_woo is None):
                        #Save product woo
                        _product_related_woo_data = {
                            "product": self._product.id,
                            "product_plataform_id": product_platform_related,
                            "method": self._platform,
                            "user": self._company.user.id
                        }

                        _woo_product = product_obj.setProductRelated(_product_related_woo_data)
                        data_response['woocommerce'] = f"The product {product_platform_related} has been saved succesfully with the next related product id {_woo_product.id}"

            _check_meli_product = product_obj.getProductRelatedID(self._product.id, 'mercado_libre')

            if(product_status == 'Active'):
                if(_check_meli_product is None):
                    product_data_meli = {
                        "product_name": product_name,
                        "product_description": product_description,
                        "product_sku": product_sku,
                        "product_price": float(product_price),
                        "product_stock": product_stock,
                        "product_weight": product_weight,
                        "product_height": product_height,
                        "product_width": product_width,
                        "product_length": product_length,
                        "product_images": images,
                        "product_categories": _categories,
                        "product_editorial": product_editorial,
                        "product_collection": product_collection,
                        "product_listing_type_id": "gold_pro",
                        "product_isbn": product_isbn,
                        "product_author": product_author
                    }
                    product_obj_meli_new = product_obj_meli.setNewProduct(product_data_meli)

                    #return Response(product_obj_meli_new)
                    if(product_obj_meli_new['status'] == 400):
                        return Response(product_obj_meli_new)
                    
                    #Save Related ID
                    data_meli_order = {
                        "product": self._product.id,
                        "product_plataform_id": product_obj_meli_new['id'],
                        "method": 'mercado_libre',
                        "user": self._company.user.id
                    }
                    
                    _meli_product = product_obj.setProductRelated(data_meli_order)

                    _data_product_price_meli = {
                        "product": self._product.id,
                        "plataform_name": "mercado_libre",
                        "product_price":  product_obj_meli_new['price'],
                        "user": self._company.user.id
                    }

                    _product_price_meli = product_obj.setProductPrice(_data_product_price_meli)
                    data_response['meli_id'] = f"The product has been created succesfully in MELI with ID {product_obj_meli_new['id']}"
                    data_response['status'] = status.HTTP_200_OK
                    
                else:
                    self.check_product_mercado_libre = _check_meli_product
                    
                    if(self.check_product_mercado_libre is None):
                        _meli_product_id = product_obj_meli.getIDProductBySKU(product_sku)
                        #Save Related ID
                        data_meli_order = {
                            "product": self._product.id,
                            "product_plataform_id": _meli_product_id,
                            "method": 'mercado_libre',
                            "user": self._company.user.id
                        }
                        _meli_product = product_obj.setProductRelated(data_meli_order)
                        self.check_product_mercado_libre = _meli_product.pk
                        data_response['relaed_meli_order'] = f"The meli product {self._product.id} has been created with ID {_meli_product_id}"

                    product_data_meli = {
                        "product_id": self.check_product_mercado_libre,
                        "product_name": product_name,
                        "product_description": product_description,
                        "product_sku": product_sku,
                        "product_price": float(product_price),
                        "product_stock": product_stock,
                        "product_weight": product_weight,
                        "product_height": product_height,
                        "product_width": product_width,
                        "product_images": images,
                        "product_length": product_length,
                        "product_editorial": product_editorial,
                        "product_collection": product_collection,
                        "product_listing_type_id": "gold_pro"
                    }

                    product_obj_meli_new = product_obj_meli.setProductUpdate(product_data_meli)
                    
                    if(product_obj_meli_new['status'] == 400):
                        return Response(product_obj_meli_new)
                    

                    if(product_obj.getProductPrice('mercado_libre') is None):
                        _data_product_price_meli = {
                            "product": self._product.id,
                            "plataform_name": "mercado_libre",
                            "product_price":  product_obj_meli_new['price'],
                            "user": self._company.user.id
                        }

                        _product_price_meli = product_obj.setProductPrice(_data_product_price_meli)
                    
                    data_response['meli_id'] = f"The product {self.check_product_mercado_libre} has been updated succesfully in MELI"
                
                    data_response['status'] = status.HTTP_200_OK
                
            return Response(data_response, data_response['status'])
        