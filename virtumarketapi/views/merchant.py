from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from virtumarketapi.models import Merchant, Good, Market, GoodType
from django.contrib.auth.models import User
from .good import GoodSerializer

class MerchantUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = (
            "id",
            "url",
            "bio",
            "profile_image",
            "booth_image",
            "company_name",
            "phone_number",
            "market"
        )
        depth = 1

class SimpleMerchantUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant
        fields = (
            "id",
            "url",
            "bio",
            "profile_image",
            "booth_image",
            "company_name",
            "phone_number",
            "market_id"
        )
        depth = 1
class MerchantSerializer(serializers.HyperlinkedModelSerializer):

    goods = GoodSerializer(many=True, read_only=True)

    class Meta:
        model = Merchant

        url = serializers.HyperlinkedIdentityField(
            view_name="merchant",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "company_name",
            "profile_image",
            "booth_image",
            "user_id",
            "market_id",
            "goods"
        )
        depth = 1

class MarketMerchantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Merchant

        fields = (
            "id",
            "url",
            "company_name",
            "profile_image",
            "bio",
            "phone_number",
            "booth_image",
            "user_id",
            "market_id",
        )
        depth = 1

class Merchants(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            merchant = Merchant.objects.get(pk=pk)

            serializer = MerchantSerializer(
                merchant,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        merchants = Merchant.objects.all()

        serializer = MerchantSerializer(
            merchants,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def inventory(self, request):

        name = self.request.query_params.get('name', None)
        good_type = self.request.query_params.get('type', None)
        market = self.request.query_params.get('market', None)

        if name is not None and market is not None:
            final_merchants = set()
            market = Market.objects.get(pk=market)
            searched_goods = Good.objects.filter(name__startswith=name)
            for good in searched_goods:
                merchant = Merchant.objects.get(pk=good.merchant_id)
                if merchant.market == market:
                    final_merchants.add(merchant)

            serializer = MarketMerchantSerializer(
                final_merchants,
                many=True,
                context={"request": request}
            )
            return Response(serializer.data)

        elif good_type is not None and market is not None:
            final_merchants = set()
            market = Market.objects.get(pk=market)
            try: 
                good_type = GoodType.objects.get(name__startswith=good_type)

            except GoodType.DoesNotExist:
                good_type = None

            searched_goods = Good.objects.filter(good_type=good_type)
            for good in searched_goods:
                merchant = Merchant.objects.get(pk=good.merchant_id)
                if merchant.market == market:
                    final_merchants.add(merchant)

            serializer = MarketMerchantSerializer(
                final_merchants,
                many=True,
                context={"request": request}
            )
            return Response(serializer.data)

