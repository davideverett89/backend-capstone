from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import GoodType

class GoodTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GoodType

        url = serializers.HyperlinkedIdentityField(
            view_name="goodtype",
            lookup_field="id"
        )

        fields = (
            "id",
            "name",
            "url"
        )
        depth = 1

class GoodTypes(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            good_type = GoodType.objects.get(pk=pk)
            serializer = GoodTypeSerializer(
                good_type,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        good_types = GoodType.objects.all()
        serializer = GoodTypeSerializer(
            good_types,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)