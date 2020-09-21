from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import GoodBasket, Basket, Good, Consumer

class GoodBasketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GoodBasket

        url = serializers.HyperlinkedIdentityField(
            view_name="goodbasket",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "date_added",
            "basket_id",
            "good_id"
        )
        depth = 1

class GoodBaskets(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            good_basket = GoodBasket.objects.get(pk=pk)
            serializer = GoodBasketSerializer(
                good_basket,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        good_baskets = GoodBasket.objects.all()
        serializer = GoodBasketSerializer(
            good_baskets,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):

        current_user = Consumer.objects.get(user=request.auth.user)

        new_good_basket = GoodBasket()
        good = Good.objects.get(pk=request.data["good_id"])
        new_good_basket.good = good
        new_good_basket.date_added = request.data["date_added"]

        try:

            basket = Basket.objects.get(consumer=current_user, payment_method=None, date_completed=None)
            new_good_basket.basket = basket
            new_good_basket.save()

            serializer = GoodBasketSerializer(
                new_good_basket,
                context={"request": request}
            )
            return Response(serializer.data)

        except Basket.DoesNotExist:

            new_basket = Basket()
            new_basket.consumer = current_user
            new_basket.payment_method_id = None
            new_basket.date_completed = None
            new_basket.save()

            new_good_basket.basket = new_basket
            new_good_basket.save()

            serializer = GoodBasketSerializer(
                new_good_basket,
                context={"request": request}
            )
            return Response(serializer.data)


