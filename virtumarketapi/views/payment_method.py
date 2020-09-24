from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
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

    def create(self, request):

        payment_method = PaymentMethod()

        consumer = Consumer.objects.get(pk=request.data["consumer_id"])

        payment_method.merchant_name = request.data["merchant_name"]
        account_number = request.data["account_number"]
        payment_method.account_number = account_number[-4:].rjust(len(account_number), "*")
        payment_method.expiration_date = request.data["expiration_date"]
        payment_method.creation_date = request.data["creation_date"]
        payment_method.consumer = consumer

        payment_method.save()

        serializer = PaymentMethodSerializer(
            payment_method,
            context={"request": request}
        )
        return Response(serializer.data)

    def destroy(self, request, pk=None):

        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
            payment_method.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentMethod.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
