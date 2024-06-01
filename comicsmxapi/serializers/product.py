from rest_framework import serializers
from ..models.Product import Product,  ProductsInventory, ProductsInventoryUpdate, ProductUpdatedLog, ProductsRelatedPlataform, ProductsPrice, ProductMeta

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['date_published', 'date_updated']
        
class ProductsInventoryUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsInventoryUpdate
        exclude = ['date_published', 'date_updated']

class ProductUpdateLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductUpdatedLog
        exclude = ['date_published', 'date_updated']

class ProductsInventorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsInventory
        exclude = ['date_published', 'date_updated']

class ProductsRelatedPlataformSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsRelatedPlataform
        exclude = ['date_published', 'date_updated']

class ProductsPriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductsPrice
        exclude = ['date_published', 'date_updated']

class ProductMetaSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductMeta
        exclude = ['date_published', 'date_updated']
