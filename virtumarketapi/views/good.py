from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from virtumarketapi.models import Good, Merchant, GoodType, UnitSize

class GoodSerializer(serializers.HyperlinkedModelSerializer):

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
            "unit_size_id",
            "url"
        )
        depth = 1

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

        print('POST request:', request.data)

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