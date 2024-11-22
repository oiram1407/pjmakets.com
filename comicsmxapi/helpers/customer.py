from ..models.Customer import Customer
from ..serializers.customer import CustomerSerializer
import json

class CustomerHelper:
    def __init__(self, customer_phone = None):
        self._customer_phone = customer_phone
        self._customer = None

    def getCustomerList(self):
        customers = Customer.objects.filter(status='Active').all()
        customer_list = CustomerSerializer(customers, many=True)

        return customer_list.data

    def getCustomerID(self):
        customer = Customer.objects.filter(phone=str(self._customer_phone)).first()

        return customer

    def setCustomer(self, _data):
        customer = CustomerSerializer(data=_data)

        if(customer.is_valid()):
            pass
        else:
            return customer.errors

        customer.save()

        return customer.data