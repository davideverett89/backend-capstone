from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from virtumarketapi.models import Consumer
from .payment_method import PaymentMethodSerializer

class ConsumerUserSerializer(serializers.ModelSerializer):

    paymentmethods = PaymentMethodSerializer(many=True, read_only=True)

    class Meta:
        model = Consumer
        fields = (
            "id",
            "url",
            "bio",
            "profile_image",
            "phone_number",
            "user_id",
            "paymentmethods"
        )
        depth = 1

class ConsumerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Consumer

        url = serializers.HyperlinkedIdentityField(
            view_name="consumer",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "bio",
            "profile_image",
            "phone_number",
            "user_id"
        )
        depth = 1

class Consumers(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            consumer = Consumer.objects.get(pk=pk)

            serializer = ConsumerSerializer(
                consumer,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        consumers = Consumer.objects.all()

        serializer = ConsumerSerializer(
            consumers,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)