from ..models import Product, ProductsRelatedPlataform, ProductsPrice
from ..serializers.product import ProductsRelatedPlataformSerializers, ProductMetaSerializers, ProductsPriceSerializers

class ProductHelper:
    def __init__(self, sku):
        self._sku = sku

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

    def getProductPrice(sel, _platform):
        _product_price = ProductsPrice.objects.filter(plataform_name=_platform).first()

        return _product_price