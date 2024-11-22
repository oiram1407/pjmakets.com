from rest_framework import status
from ...models.Companies import CompaniesPlataformsRelated
from ...models.Product import Product, ProductsRelatedPlataform
from ...models.Order import OrderPlataformRelated
import json
import requests
from base64 import b64encode

class WooCommerceHelper:

    def __init__(self):
        self._current_plataform = 'woocommerce'

    def WoocommerAccountByCompany(self, company_related):
        self._ini_company = company_related
        company_plataform = CompaniesPlataformsRelated.objects.get(company_id=company_related.id, plataform=self._current_plataform)
        self._company = company_plataform
        self._company_data = json.loads(self._company.data)
        self._company_id = self._company.id
        self._api_url = self._company_data['api_url']
        self._user_api = self._company_data['user']
        self._password_api = self._company_data['password']
        
        return self._company
    
    def WoocommerceAccountByURL(self, url):
        company_plataform = CompaniesPlataformsRelated.objects.get(data__contains=url, plataform=self._current_plataform)
        self._company = company_plataform
        self._company_data = json.loads(self._company.data)
        self._company_id = self._company.id
        self._api_url = self._company_data['api_url']
        self._user_api = self._company_data['user']
        self._password_api = self._company_data['password']

        return self._company

    def checkOrder(self, _order_id):
        self._order = OrderPlataformRelated.objects.filter(order_plataform_id=_order_id).first()
        
        return self._order
    
    def getOrderData(self, _order_id):
        url = self._api_url+"/orders/"+_order_id

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic '+b64encode(f"{self._user_api}:{self._password_api}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("GET", url, headers=headers)
        order_data = response.json()
        _order_items = order_data['line_items']
        items = {}
        item_count = 0
        
        for i in range(len(_order_items)):
            items[item_count] = {
                "sku": _order_items[i]['sku'],
                "quantity": _order_items[i]['quantity'],
                "total": _order_items[i]['total'],
                "total_tax": _order_items[i]['total_tax'],
            }

            item_count+=1

        response_order_data = {
            "order_plataform_id": self._current_plataform+'_'+str(order_data['id']),
            "plataform": self._current_plataform,
            "total_amount": order_data['total'],
            "paid_amount": order_data['total'],
            "date_order": order_data['date_created'],
            "company": company.id,
            "user": user.id,
            "data": json.dumps(items)
        }

        return response_order_data
        
    def fixStatus(selef, current_status):
        if(current_status == 'processing'):
            return 'paid'
        elif(current_status == 'pendding'):
            return 'pendding'
        elif(current_status == 'cancelled'):
            return 'failed'
        elif(current_status == 'refunded'):
            return 'failed'
        elif(current_status == 'trash'):
            return 'failed'
        elif(current_status == 'on-hold'):
            return 'paid'
        elif(current_status == 'completed'):
            return 'completed'

    def getProductBySKU(self, _sku):
        product = Product.objects.get(sku=_sku)

        self._product_id = product.id
        
        return self._product_id

    def getProductRelated(self):
        product_related = ProductsRelatedPlataform.objects.get(product_id=self._product_id, method=self._current_plataform)
        
        self._product_related_id = product_related.product_plataform_id
        
        return self._product_related_id

    def setInventory(self, new_stock):
        product_tmp = self._product_related_id.split(self._ini_company.name+'_#')
        self._product_related_id = product_tmp[1]
        url = self._api_url+"/products/"+str(self._product_related_id)

        payload = json.dumps({
            "stock_quantity": int(new_stock)
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic '+b64encode(f"{self._user_api}:{self._password_api}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        response = response.json()

        if('id' in response):
            return response
        elif('code' in response):
            if(response['code'] == 'woocommerce_rest_product_invalid_id'):
                return {"msg":"error to update inventory in woocommerce shop"}
        
