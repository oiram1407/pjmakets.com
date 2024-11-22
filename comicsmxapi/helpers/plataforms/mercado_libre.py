from ...models.Companies import CompaniesPlataformsRelated
from ...generals import Generals as cfg
from unidecode import unidecode
import requests
import json

class MercadoLibreHelper:
    def __init__(self, company):
        self._company = company
        self._current_plataform = 'mercado_libre'
        self._api_meli = cfg.getSettingParammeter('meli_api_url')

    def getDataAccount(self):
        company_plataform_related = CompaniesPlataformsRelated.objects.get(company=self._company.id, plataform=self._current_plataform)
        meli_data = json.loads(company_plataform_related.data)
        self._meli_data = meli_data
        self._grant_type = meli_data['grant_type']
        self._app_id = meli_data['app_id']
        self._client_secret = meli_data['client_secret']
        self._user_id = meli_data['user_id']

        return self._meli_data 
    
    def getTokenAccount(self):
        self.getDataAccount()

        url = self._api_meli+"/oauth/token"

        payload = 'grant_type='+self._grant_type+'&client_id='+self._app_id+'&client_secret='+self._client_secret
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        self._access_token = response['access_token']

        return self._access_token
    
    def getIDProductBySKU(self, sku):
        self.getTokenAccount()
        self._sku = sku

        url = self._api_meli+'/users/'+self._user_id+'/items/search?seller_sku='+sku

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("GET", url, headers=headers)
        response = response.json()

        meli_items = response['results']

        if len(meli_items) <= 0:
            return None
        else:
            self._meli_item_id = meli_items[0]

            return self._meli_item_id
        
    def getProductDataByID(self, new_inventory):
        self._api_item = self._api_meli+'/items'
        self._api_item_url = self._api_item+'/'+self._meli_item_id
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("GET", self._api_item_url, headers=headers)
        response = response.json()

        variations_len = len(response['variations']) 

        if variations_len > 0: #If exists variations
            _variations_data = {}
            _variations_data_count = 0

            for i in range(variations_len):
                _variations_data_tmp = {}
                _variation = response['variations'][i]
                url_variations = self._api_item_url+'/variations/'+str(_variation['id'])

                response_variations = requests.request("GET", url_variations, headers=headers)
                response_variations = response_variations.json()
                flag_product = 0

                for i in range(len(response_variations['attributes'])):
                    attributes = response_variations['attributes']
                    if attributes[i]['id'] == "SELLER_SKU":
                        if attributes[i]['value_name'] == self._sku:
                            flag_product = 1

                _variations_data_tmp['id'] = response_variations['id']
                _variations_data_tmp['available_quantity'] = new_inventory if flag_product else response_variations['available_quantity']
                _variations_data[_variations_data_count] = _variations_data_tmp
                _variations_data_count+=1

            return _variations_data.values()
        else:
            return new_inventory

    def setInventory(self, new_inventory, mode = 0):
        variations = self.getProductDataByID(new_inventory)
        
        if(mode == 0):
            data_inventory = {
                'variations': list(variations)
            }

        else:
            data_inventory = {
                "available_quantity": variations
            }
        

        data_inventory = json.dumps(data_inventory)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("PUT", self._api_item_url, headers=headers, data=data_inventory)

        return response.json()

    def calcPrice(self, data): 
        meli_price = 0
        shipping_price = 0
        _original_pice = float(data['product_price']) + float(10)

        api_price = f"{self._api_meli}/sites/MLM/listing_prices?price={_original_pice}&category_id=MLM1196"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("GET", api_price, headers=headers)

        _prices = response.json()

        for i in range(len(_prices)):
            _price = _prices[i]
            if(_price['listing_type_id'] == data['product_listing_type_id']):
                meli_price += _original_pice
                meli_price += float(_price['sale_fee_amount'])
                meli_price += (float(_price['sale_fee_amount'])*float(1/_price['sale_fee_details']['percentage_fee']))

        meli_price = round(meli_price, 2)

        return meli_price

    def calcShipping(self, data):
        _weight = int(float(data['product_weight'])*1000)
        _product_height = round(float(data['product_height']))
        _product_width = round(float(data['product_width']))
        _product_length = round(float(data['product_length']))
        _url = f"{self._api_meli}/users/{self._user_id}/shipping_options/free?dimensions={_product_height}x{_product_width}x{_product_length},{_weight}&verbose=TRUE&item_price={data['product_price']}&listing_type_id={data['product_listing_type_id']}&mode=me2&condition=new&logistic_type=xd_drop_off"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("GET", _url, headers=headers)

        _shp_price = response.json()
        shp_price = 0
        if(_shp_price['coverage']['all_country']['discount']['promoted_amount'] > 0 ):
            shp_price += _shp_price['coverage']['all_country']['discount']['promoted_amount']
        else:
            shp_price += _shp_price['coverage']['all_country']['list_cost']
            
        return shp_price
    
    def serarchISBN(self, title, serie, editorial):
        self._google_books_api = 'https://www.googleapis.com/books/v1/'

        headers = {
            'Content-Type': 'application/json',
        }

        serie = serie.lower()
        _params = [
            ("q", title),
            #("publisher", editorial)
        ]
        #komi can't communicate

        response = requests.request("GET", f"{self._google_books_api}volumes", headers=headers, params=_params)
        _response = response.json()
        _items = _response['items']

        author = ""
        isbn = ""
        for i in range(len((_items))):
            _item = _items[i]
            _book_info = _item['volumeInfo']
            _book_title = unidecode(_book_info['title'].lower())

            if unidecode(serie) in _book_title:
                if 'authors' in _book_info:
                    _authors = _book_info["authors"]
                    for j in range(len(_authors)):
                        author = _authors[j]

                if 'industryIdentifiers' in _book_info:
                    _isbn = _book_info['industryIdentifiers'] #['ISBN_13']
                    for j in range(len(_isbn)):
                        _isbn_t = _isbn[j]
                        if(_isbn_t['type'] == "ISBN_13"):
                            isbn = _isbn_t['identifier']

        return (author, isbn)
    
    def setNewProduct(self, product_data):
        self.getTokenAccount()

        _data = {
            "product_price": product_data['product_price'],
            "product_listing_type_id": product_data['product_listing_type_id'],
        }

        meli_price = self.calcPrice(_data)+10

        if(meli_price > 299):
            meli_price += self.calcShipping(product_data)

        isbn = None
        author = None

        isbn = product_data['product_isbn'] if(product_data['product_isbn']) else (isbn if(isbn) else '9786075787640')
        author = product_data['product_author'] if(product_data['product_author']) else (author if(author) else product_data['product_editorial'])

        if ((isbn is None) and (author is None)):
            (author, isbn) = self.serarchISBN(product_data['product_name'], product_data['product_collection'], product_data['product_editorial'])
            isbn = isbn if(isbn) else '9786075787640'
            author = author if(author) else product_data['product_editorial']
            
        data_new_product = {
            "title": (product_data['product_name'][:57] + '...') if len(product_data['product_name']) > 57 else product_data['product_name'],
            "description": product_data['product_description'],
            "category_id": "MLM1196",
            "price": round(meli_price,2),
            "currency_id": "MXN",
            "available_quantity": product_data['product_stock'],
            "pictures": product_data['product_images'],
            "buying_mode": "buy_it_now",
            "sale_terms": [
                {
                    "id": "WARRANTY_TYPE",
                    "name": "Tipo de garantía",
                    "value_id": "6150835",
                    "value_name": "Sin garantía",
                    "value_struct": None,
                    "values": [
                        {
                            "id": "6150835",
                            "name": "Sin garantía",
                            "struct": None
                        }
                    ],
                    "value_type": "list"
                }
            ],
            "listing_type_id": product_data['product_listing_type_id'],
            "attributes": [
                {
                    "id": "AUTHOR",
                    "value_name": author
                },
                {
                    "id": "ACCESSORIES_INCLUDED",
                    "value_name": "No"
                },
                {
                    "id": "BOOKS_NUMBER_PER_SET",
                    "value_name": "1"   
                },
                {
                    "id": "BOOK_COLLECTION",
                    "value_name": product_data['product_collection']
                },
                {
                    "id": "BOOK_COVER",
                    "value_name": "Blanda"
                },
                {
                    "id": "BOOK_COVER_MATERIAL",
                    "value_name": "Papel"
                },
                {
                    "id": "BOOK_EDITION",
                    "value_name": "1"
                },
                {
                    "id": "BOOK_GENRE",
                    "value_name": "Aventura,Manga"
                },
                {
                    "id": "BOOK_PUBLISHER",
                    "value_name": product_data['product_editorial']
                },
                {
                    "id": "BOOK_SERIE",
                    "value_name": product_data['product_collection']
                },
                {
                    "id": "BOOK_SIZE",
                    "value_name": "Manga"
                },
                {
                    "id": "BOOK_SUBGENRES",
                    "value_name": "Manga"
                },
                {
                    "id": "BOOK_TITLE",
                    "value_name": product_data['product_collection']
                },
                {
                    "id": "BOOK_VERSION",
                    "value_name": "Primera"
                },
                {
                    "id": "BOOK_VOLUME",
                    "value_name": "1"
                },
                {
                    "id": "CO_AUTHORS",
                    "value_name": "-1"
                },
                {
                    "id": "HEIGHT",
                    "value_name": f"{product_data['product_height']} cm"
                },
                {
                    "id": "IS_WRITTEN_IN_CAPITAL_LETTERS",
                    "value_name": "No"
                },
                {
                    "id": "ITEM_CONDITION",
                    "value_name": "Nuevo"
                },
                {
                    "id": "LANGUAGE",
                    "value_name": "Español"
                },
                {
                    "id": "MAX_RECOMMENDED_AGE",
                    "value_name": "100 años"
                },
                {
                    "id": "MIN_RECOMMENDED_AGE",
                    "value_name": "8 años"
                },
                {
                    "id": "NARRATION_TYPE",
                    "value_name": "Manga"
                },
                {
                    "id": "PAGES_NUMBER",
                    "value_name": "150"
                },
                {
                    "id": "PUBLICATION_YEAR",
                    "value_name": "201"
                },
                {
                    "id": "TRANSLATORS",
                    "value_name": product_data['product_editorial']
                },
                {
                    "id": "WEIGHT",
                    "value_name": f"{product_data['product_weight']} g"
                },
                {
                    "id": "WIDTH",
                    "value_name": f"{product_data['product_width']} cm"
                },
                {
                    "id": "WITH_AUGMENTED_REALITY",
                    "value_name": "No"
                },
                {
                    "id": "WITH_COLORING_PAGES",
                    "value_name": "No"
                },
                {
                    "id": "WITH_INDEX",
                    "value_name": "Sí"
                },
                {
                    "id": "SELLER_SKU",
                    "value_name": product_data['product_sku']
                },
                {
                    "id": "GTIN",
                    "value_name": isbn
                }
            ],
            "warranty": "Sin garantía",
            "domain_id": "MLM-BOOKS",
            "shipping": {
                "mode": "me2",
                "methods": [],
                "tags": [],
                "dimensions": None,
                "local_pick_up": False,
                "free_shipping": False,
                "logistic_type": "xd_drop_off",
                "store_pick_up": False
            },
            "variations": [],
            "channels": [
                "marketplace"
            ]
        }
        
        data_new_product = json.dumps(data_new_product)
        self._api_item_create = f"{self._api_meli}/items"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("POST", self._api_item_create, headers=headers, data=data_new_product)
        response_json = response.json()

        if(response_json['id']):
            self.updateDescriptionItem(response_json['id'], product_data['product_description'])

        return response_json

    def setProductUpdate(self, product_data):
        self.getTokenAccount()
        self._meli_item_id = product_data['product_id']

        _data = {
            "product_price": product_data['product_price'],
            "product_listing_type_id": product_data['product_listing_type_id'],
        }

        meli_price = self.calcPrice(_data)

        if(meli_price > 299):
            meli_price += self.calcShipping(product_data)

        data_new_product = {
            "title": (product_data['product_name'][:57] + '...') if len(product_data['product_name']) > 57 else product_data['product_name'],
            "price": round(meli_price,2),
            "currency_id": "MXN",
            "pictures": product_data['product_images'],
            "attributes": [
                {
                    "id": "SELLER_SKU",
                    "value_name": product_data['product_sku']
                }
            ]
        }
        
        data_new_product = json.dumps(data_new_product)
        self._api_item_create = f"{self._api_meli}/items/{product_data['product_id']}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("PUT", self._api_item_create, headers=headers, data=data_new_product)
        response = response.json()

        if(response['status'] == 400):
            self._sku = product_data['product_sku']
            self.getProductDataByID(product_data['product_id'])
        
            response = self.setInventory(product_data['product_stock'], 0)
            return response

        self.setInventory(product_data['product_stock'], 1)

        if(response['id']):
            self.updateDescriptionItem(response['id'], product_data['product_description'])

        return response

    def updateDescriptionItem(self, product_id, product_desc):
        self.getTokenAccount()

        data = {
            "plain_text": product_desc
        }

        data = json.dumps(data)

        self._api_item_description = f"{self._api_meli}/items/{product_id}/description?api_version=2"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self._access_token
        }

        response = requests.request("PUT", self._api_item_description, headers=headers, data=data)

        return response.json()

    def fixStatus(selef, current_status):
        if(current_status == 'paid'):
            return 'paid'
        elif(current_status == 'payment_required'):
            return 'pendding'
        elif(current_status == 'payment_in_process'):
            return 'pendding'
        elif(current_status == 'partially_paid'):
            return 'pendding'
        elif(current_status == 'partially_refunded'):
            return 'failed'
        elif(current_status == 'pending_cancel'):
            return 'failed'
        elif(current_status == 'cancelled'):
            return 'failed'
        elif(current_status == 'delivered'):
            return 'completed'
