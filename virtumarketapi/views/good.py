from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtumarketapi.models import Good, Merchant, GoodType, UnitSize, GoodBasket
from .good_basket import GoodBasketSerializer

class GoodSerializer(serializers.HyperlinkedModelSerializer):

    number_on_order = serializers.SerializerMethodField()

    class Meta:
        model = Good

        url = serializers.HyperlinkedIdentityField(
            view_name="good",
            lookup_field="id"
        )

        fields = (
            "id",
            "name",
            "image",
            "price",
            "description",
            "quantity",
            "good_type_id",
            "merchant_id",
            "unit_size",
            "url",
            "number_on_order"
        )
        depth = 1

    def get_number_on_order(self, obj):
        good_baskets = GoodBasket.objects.filter(good=obj)
        return len(good_baskets)

class Goods(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            good = Good.objects.get(pk=pk)
            serializer = GoodSerializer(
                good,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        goods = Good.objects.all()

        serializer = GoodSerializer(
            goods,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):

        new_good = Good()
        merchant = Merchant.objects.get(user=request.auth.user)
        good_type = GoodType.objects.get(pk=request.data["good_type_id"])
        unit_size = UnitSize.objects.get(pk=request.data["unit_size_id"])

        new_good.name = request.data["name"]
        new_good.image = request.data["image"]
        new_good.price = request.data["price"]
        new_good.description = request.data["description"]
        new_good.quantity = request.data["quantity"]
        new_good.good_type = good_type
        new_good.merchant = merchant
        new_good.unit_size = unit_size

        new_good.save()

        serializer = GoodSerializer(
            new_good,
            context={"request": request}
        )
        return Response(serializer.data)

    def destroy(self, request, pk=None):

        try:
            good = Good.objects.get(pk=pk)
            good.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Good.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk=None):

        good = Good.objects.get(pk=pk)
        unit_size = UnitSize.objects.get(pk=request.data["unit_size_id"])

        good.name = request.data["name"]
        good.image = request.data["image"]
        good.price = request.data["price"]
        good.description = request.data["description"]
        good.quantity = request.data["quantity"]
        good.unit_size = unit_size

        good.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
