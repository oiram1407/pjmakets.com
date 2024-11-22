from ..models.Order import OrderPlataformRelated
from ..serializers.order import OrderPlataformRelatedSerializers
import json

class Order:
    def __init__(self, id_order_plataform = None):
        self._id_order_plataform = id_order_plataform

    def getOrderID(self):
        order = OrderPlataformRelated.objects.get(order_plataform_id=self._id_order_plataform)
        self._id_order = order.pk

        return self._id_order
    
    def setNewOrderStatus(self, new_status):
        order_status = OrderPlataformRelated.objects.filter(pk=self._id_order).update(status=new_status)

        return order_status

    def getOrderList(self, params):

        try:
            orders = OrderPlataformRelated.objects.filter(plataform=params['plataform'], status=params['status']).all()
            orders_list = OrderPlataformRelatedSerializers(orders, many=True)
        except:
            orders = OrderPlataformRelated.objects.all()
            orders_list = OrderPlataformRelatedSerializers(orders, many=True)

        return orders_list.data

    def updateOderStatus(self, params):
        order = OrderPlataformRelated.objects.filter(pk=params['id']).update(status=params['status'])

        return order

        
