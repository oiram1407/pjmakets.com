from ..models.Order import OrderPlataformRelated
import json

class Order:
    def __init__(self, id_order_plataform):
        self._id_order_plataform = id_order_plataform

    def getOrderID(self):
        order = OrderPlataformRelated.objects.get(order_plataform_id=self._id_order_plataform)
        self._id_order = order.pk

        return self._id_order
    
    def setNewOrderStatus(self, new_status):
        order_status = OrderPlataformRelated.objects.filter(pk=self._id_order).update(status=new_status)

        return order_status

