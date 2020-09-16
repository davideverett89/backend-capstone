from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import Market
from .merchant import MarketMerchantSerializer

class MarketSerializer(serializers.HyperlinkedModelSerializer):

    merchants = MarketMerchantSerializer(many=True, read_only=True)

    class Meta:
        model = Market

        url = serializers.HyperlinkedIdentityField(
            view_name="market",
            lookup_field="id"
        )

        fields = (
            "id",
            "name",
            "image",
            "description",
            "zip_code",
            "merchants",
            "url"
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