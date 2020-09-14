from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import UnitSize

class UnitSizeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UnitSize

        url = serializers.HyperlinkedIdentityField(
            view_name="unit_size",
            lookup_field="id"
        )

        fields = (
            "id",
            "name"
        )
        depth = 1

class UnitSizes(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            unit_size = UnitSize.objects.get(pk=pk)
            serializer = UnitSizeSerializer(
                unit_size,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        unit_sizes = UnitSize.objects.all()
        serializer = UnitSizeSerializer(
            unit_sizes,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)