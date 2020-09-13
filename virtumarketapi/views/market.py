from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import Market

class MarketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Market

        fields = (
            "id",
            "name",
            "zip_code"
        )
        depth = 1

class Markets(ViewSet):

    def retrieve(self, request, pk=None):
        
        try:
            market = Market.objects.get(pk=pk)
            serializer = MarketSerializer(market, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True, context={"request": request})
        return Response(serializer.data)