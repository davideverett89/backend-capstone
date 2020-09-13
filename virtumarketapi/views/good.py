from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
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
            "price",
            "description",
            "quantity",
            "good_type_id",
            "merchant_id",
            "unit_size_id"
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