from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from virtumarketapi.models import PaymentMethod, Consumer

class PaymentMethodSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PaymentMethod

        url = serializers.HyperlinkedIdentityField(
            view_name="paymentmethod",
            lookup_field="id"
        )

        fields = (
            "id",
            "merchant_name",
            "account_number",
            "expiration_date",
            "creation_date",
            "consumer_id",
            "url"
        )
        depth = 1

class PaymentMethods(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
            serializer = PaymentMethodSerializer(
                payment_method,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        payment_methods = PaymentMethod.objects.all()
        serializer = PaymentMethodSerializer(
            payment_methods,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)
