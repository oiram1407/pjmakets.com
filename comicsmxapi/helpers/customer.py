from ..models.Customer import Customer

class CustomerHelper:
    def __init__(self, customer_phone) -> None:
        self._customer_phone = customer_phone

    def getCustomerID(self):
        customer = Customer.objects.filter(phone=str(self._customer_phone)).first()

        return customer
