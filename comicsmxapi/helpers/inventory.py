from rest_framework import status
from rest_framework.response import Response
from ..models import Product, ProductsInventory
from ..serializers.product import ProductsInventoryUpdateSerializers, ProductUpdateLogSerializers, ProductsInventorySerializers

class InventoryHelper:

    def __init__(self, product, quantity):
        self._quanity = quantity
        self._product_id = product.id
        self._product = product
    
    def getProductInventory(self):
        inventory = ProductsInventory.objects.filter(product=self._product_id).first()

        return inventory

    def setProductInventoyUpdate(self, data):
        inventory_update_data = {
            "product": self._product_id,
            "quantity": self._quanity if(self._quanity >0) else data['quantity'],
            "method_update": data['method_update'],
            "action_type": data['action_type'],
            "user": data['user']
        }

        if('current_inventory' in data):
            inventory_update_data['status'] = 'Active' if(data['current_inventory'] < data['quantity']) else 'Inactive'

        inventory_update_serializer = ProductsInventoryUpdateSerializers(data=inventory_update_data)

        if(inventory_update_serializer.is_valid()):
            pass
        else:
            return Response(inventory_update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        inventory_update = inventory_update_serializer.save()

        return inventory_update

    def setPoductUpdateLog(self, data):
        update_log_data = {
            "product": self._product_id,
            "method": data['method'],
            "action": data['action'],
            "action_type": data['action_type'],
            "user": data['user']
        }
    
        update_log_serializer = ProductUpdateLogSerializers(data=update_log_data)

        if(update_log_serializer.is_valid()):
            pass
        else:
            return Response(update_log_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        update_log = update_log_serializer.save()

        return update_log

    def setProductInventory(self, data):
        product_inventory_serializer = ProductsInventorySerializers(data=data)

        if(product_inventory_serializer.is_valid()):
            pass
        else:
            return Response(product_inventory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        product_inventory = ProductsInventory.objects.filter(product=data['product']).update(quantity=data['quantity'])

        return product_inventory
    
    def setNewProductInventory(self, _data):
        _product_data = {
            "product": self._product_id,
            "quantity": self._quanity,
            "user": _data['user']
        }
        
        _product_inventory = ProductsInventorySerializers(data=_product_data)

        if(_product_inventory.is_valid()):
            pass
        else:
            return _product_inventory.errors
        
        product_inventory = _product_inventory.save()

        return product_inventory
    