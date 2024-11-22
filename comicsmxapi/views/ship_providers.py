from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import ShipProviders
from ..serializers.ship_provider import ShipProvidersSerializers

class ShipProvidersView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        try:
            _slug = request.query_params['slug']
            if _slug != None:
                shipProv_list = ShipProviders.objects.get(provider_slug=_slug, status="Active")
                serializer = ShipProvidersSerializers(shipProv_list)

        except:
            shipProv_list = ShipProviders.objects.filter(status="Active").all()
            serializer = ShipProvidersSerializers(shipProv_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)