from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from virtumarketapi.models import Basket, GoodBasket, Consumer
from .good import GoodSerializer

class BasketSerializer(serializers.HyperlinkedModelSerializer):

    goods = GoodSerializer(many=True, read_only=True)

    class Meta:
        model = Basket
        
        url = serializers.HyperlinkedIdentityField(
            view_name="basket",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "date_completed",
            "consumer_id",
            "payment_method_id",
            "goods"
        )
        depth = 1

class Baskets(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            basket = Basket.objects.get(pk=pk)
            serializer = BasketSerializer(
                basket,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        baskets = Basket.objects.all()

        serializer = BasketSerializer(
            baskets,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def current(self, request, pk=None):

        consumer = Consumer.objects.get(pk=pk)

        try:

            current_basket = Basket.objects.get(consumer=consumer, payment_method=None)

            serializer = BasketSerializer(
                current_basket,
                context={"request": request}
            )
            return Response(serializer.data)

        except Basket.DoesNotExist as ex:
            return Response({}, status=status.HTTP_204_NO_CONTENT)