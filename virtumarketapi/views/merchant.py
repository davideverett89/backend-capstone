from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from virtumarketapi.models import Merchant, Good
from django.contrib.auth.models import User
from .good import GoodSerializer

# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         url = serializers.HyperlinkedIdentityField(
#             view_name="user",
#             lookup_field="id"
#         )
#         fields = (
#             "id",
#             "first_name",
#             "last_name",
#             "date_joined",
#             "email"
#         )
class MerchantSerializer(serializers.HyperlinkedModelSerializer):

    # user = UserSerializer()

    goods = GoodSerializer(many=True, read_only=True)

    class Meta:
        model = Merchant

        url = serializers.HyperlinkedIdentityField(
            view_name="merchant",
            lookup_field="id"
        )

        fields = (
            "id",
            "url",
            "company_name",
            "image",
            "phone_number",
            "user_id",
            "market_id",
            "goods"
        )
        depth = 1

class Merchants(ViewSet):

    def retrieve(self, request, pk=None):

        try:
            merchant = Merchant.objects.get(pk=pk)

            serializer = MerchantSerializer(
                merchant,
                context={"request": request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        merchants = Merchant.objects.all()

        serializer = MerchantSerializer(
            merchants,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False)
    def current_user(self, request):
        user = self.request.user

        merchant = Merchant.objects.get(user_id=user.id)
        
        serializer = MerchantSerializer(
        merchant,
        context={"request": request}
        )
        return Response(serializer.data)
