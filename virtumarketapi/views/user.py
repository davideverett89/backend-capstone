from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from virtumarketapi.models import Merchant, Consumer, Market
from rest_framework.decorators import action
from rest_framework import status
from .merchant import MerchantUserSerializer
from .consumer import ConsumerUserSerializer
from .merchant import SimpleMerchantUserSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):

    merchant = MerchantUserSerializer()
    consumer = ConsumerUserSerializer()

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
            "merchant",
            "consumer"
        )
        depth = 1

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

class Users(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(
                user,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        users = User.objects.all()
        serializer = UserSerializer(
            users,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request, pk=None):

        user = User.objects.get(pk=pk)

        if Merchant.objects.filter(user=user).exists():
            merchant = Merchant.objects.get(user=user)
            market = Market.objects.get(pk=request.data["market_id"])

            user.username = request.data["username"]
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            user.email = request.data["email"]
            user.save()

            merchant.company_name = request.data["company_name"]
            merchant.profile_image = request.data["profile_image"]
            merchant.booth_image = request.data["booth_image"]
            merchant.phone_number = request.data["phone_number"]
            merchant.bio = request.data["bio"]
            merchant.market = market
            merchant.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)


        if Consumer.objects.filter(user=user).exists():
            consumer = Consumer.objects.get(user=user)

            user.username = request.data["username"]
            user.first_name = request.data["first_name"]
            user.last_name = request.data["last_name"]
            user.email = request.data["email"]
            user.save()

            consumer.profile_image = request.data["profile_image"]
            consumer.phone_number = request.data["phone_number"]
            consumer.bio = request.data["bio"]
            consumer.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)