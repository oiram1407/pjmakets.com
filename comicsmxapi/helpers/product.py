from ..models import Product, ProductsRelatedPlataform, ProductsPrice, ProductMeta
from ..serializers.product import ProductsRelatedPlataformSerializers, ProductMetaSerializers, ProductsPriceSerializers

class ProductHelper:
    def __init__(self, sku, id = None):
        self._sku = sku
        self._id = id

    def getProductBySKU(self):
        product = Product.objects.filter(sku=self._sku).first()
        self._product = product

        return self._product
    
    def getProductRelatedID(self, id_product, platform):
        product_related = ProductsRelatedPlataform.objects.filter(product=id_product).filter(method=platform).first()

        if product_related:
            return product_related.product_plataform_id
        else:
            return None

    def getProductByRelatedID(self, id_product, platform):
        product_related = ProductsRelatedPlataform.objects.filter(product_plataform_id=id_product).filter(method=platform).first()

        if product_related:
            product = Product.objects.filter(pk=product_related.product_id).first()
            self._product=product
            return product
        else:
            return None
    
    def getProduct(self, id_product):
        product = Product.objects.filter(pk=id_product).first()

        if product:
            return product
        else:
            return None

    def setProductRelated(self, _data):
        product_related = ProductsRelatedPlataformSerializers(data=_data)
        
        if(product_related.is_valid()):
            pass
        else:
            return product_related.errors
        
        self.product_related = product_related.save()

        return self.product_related

    def fixProductStatusWoo(self, current_status):

        if(current_status == 'publish'):
            new_status = 'Active'
        else:
            new_status = 'Inactive'

        return new_status

    def setProductMeta(self, _data):
        _product_meta = ProductMetaSerializers(data=_data)

        if(_product_meta.is_valid()):
            pass
        else:
            return _product_meta.errors
        
        product_meta = _product_meta.save()

        return product_meta
    
    def setProductPrice(self, _data):
        _product_price = ProductsPriceSerializers(data=_data)

        if(_product_price.is_valid()):
            pass
        else:
            return _product_price.errors
        
        product_price = _product_price.save()

        return product_price

    def getProductPrice(self, _platform):
        _product_price = ProductsPrice.objects.filter(product_id=self._product.id,plataform_name=_platform).first()

        return _product_price

    def updateProductData(self, _id_product, _data):
        product = Product.objects.filter(pk=_id_product).update(name=_data['name'],sku=_data['sku'],status=_data['status'])

        return product

    def updateProductDataMeta(self, _id_product, _data):
        product_meta = ProductMeta.objects.filter(product=_id_product).update(description=_data['description'],images=_data['images'],weight=_data['weight'],height=_data['height'],width=_data['width'],length=_data['length'])

        return product_meta

    def updateProductDataPrice(self, _id_product, _data):
        product_meta = ProductsPrice.objects.filter(product=_id_product,plataform_name=_data['plataform_name']).update(product_price=_data['product_price'])

        return product_meta