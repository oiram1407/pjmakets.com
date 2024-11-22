from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..generals import Generals
from ..helpers.customer import CustomerHelper
import requests
import json

class CustomersView(APIView):
    def get(self, request):
        customers = CustomerHelper()

        return Response(customers.getCustomerList(), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        customer_obj = CustomerHelper(data['phone'])
        customer_obj_f = customer_obj.getCustomerID()
            
        if(customer_obj_f is None):
            customer = customer_obj.setCustomer(data)

            return Response(customer, status=status.HTTP_200_OK)

        return Response({
            "msg": "The Customer already exists"
        }, status=status.HTTP_200_OK)
            