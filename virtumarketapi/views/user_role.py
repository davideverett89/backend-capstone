from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from virtumarketapi.models import Merchant, Consumer
from .merchant import SimpleMerchantUserSerializer

class SimpleUserSerializer(serializers.HyperlinkedModelSerializer):

    merchant = SimpleMerchantUserSerializer()

    class Meta:
        model = User

        url = serializers.HyperlinkedIdentityField(
            view_name="merchant_user",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "merchant"
        )
        depth = 1

class UserRoles(ViewSet):

    def retrieve(self, request, pk=None):

        try:

            user = User.objects.get(pk=pk)
            serializer = SimpleUserSerializer(
                user,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)