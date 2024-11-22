from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..generals import Generals as cfg
from ..helpers.order import Order

class OrderView(APIView):
    def __init__(self):
        pass

    def get(self, request):
        order_obj = Order()
        orders_list = order_obj.getOrderList(request.query_params) 

        return Response(orders_list, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data

        try:
            order_obj = Order()
            orders_up = order_obj.updateOderStatus(data) 

            return Response({"msg": "Updated successfuly"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)