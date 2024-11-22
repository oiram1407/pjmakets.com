from rest_framework import status
from ...models.Companies import CompaniesPlataformsRelated
from ...models.Product import Product, ProductsRelatedPlataform
from ...models.Order import OrderPlataformRelated
from ...generals import Generals as cfg
import datetime
import json
import requests
from base64 import b64encode

class WalmartHelper:
    def __init__(self, company):
        now = datetime.datetime.now()
        date_string = now.strftime("%Y%m%d%H%M%S")
        self._correlaton = str(int(date_string))
        self._company = company
        self._current_plataform = 'walmart'
        self._svc_name = 'pjmakets account'
        self._api_walmart = cfg.getSettingParammeter('walmart_api_url')

    def WalmartAccountByCompany(self):
        company_plataform_related = CompaniesPlataformsRelated.objects.get(company=self._company, plataform=self._current_plataform)
        walmart_data = json.loads(company_plataform_related.data)
        self._walmart_data = walmart_data
        self._client_id = walmart_data['client_id']
        self._client_secret = walmart_data['client_secret']
        self._partner_id = walmart_data['partner_id']
        self._account_encode = self._client_id+':'+self._client_secret
        self._basic_encoded = b64encode(bytes(self._account_encode, "UTF-8")).decode("utf-8")
        
        return self._walmart_data

    def getTokenAccount(self):
        self.WalmartAccountByCompany()

        url = self._api_walmart+"/v3/token"

        payload = 'grant_type=client_credentials'
        headers = {
            'WM_PARTNER.ID': self._partner_id,
            'WM_MARKET': 'mx',
            'WM_QOS.CORRELATION_ID': bytes(self._correlaton, "UTF-8"),
            'WM_SVC.NAME': self._svc_name,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': "Basic "+self._basic_encoded
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        self._access_token = response['access_token']

        return self._access_token

    def findItemBySKU(self, sku):
        self.getTokenAccount()
        
        url = self._api_walmart+"/v3/items/"+sku
        payload = 'grant_type=client_credentials'
        headers = {
            'WM_PARTNER.ID': self._partner_id,
            'WM_SEC.ACCESS_TOKEN': self._access_token,
            'WM_QOS.CORRELATION_ID': bytes(self._correlaton, "UTF-8"),
            'WM_SVC.NAME': self._svc_name,
            'WM_MARKET': 'mx',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': "Basic "+self._basic_encoded
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()

        if(response['totalItems'] < 1):
            return None

        return response['ItemResponse'][0]

    def setItem(self, data):
        self.getTokenAccount()
        return data