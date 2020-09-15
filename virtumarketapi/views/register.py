import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from virtumarketapi.models import Merchant
from virtumarketapi.models import Consumer
from virtumarketapi.models import Market


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            
            if Merchant.objects.filter(user=authenticated_user).exists():
                merchant = Merchant.objects.get(user=authenticated_user)
                data = json.dumps({"valid": True, "token": token.key, "user_role": "merchant", "id": merchant.id, "uid": authenticated_user.id})
                return HttpResponse(data, content_type='application/json')
            if Consumer.objects.filter(user=authenticated_user).exists():
                consumer = Consumer.objects.get(user=authenticated_user)
                data = json.dumps({"valid": True, "token": token.key, "user_role": "consumer", "id": consumer.id, "uid": authenticated_user.id})
                return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_merchant(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    merchant = Merchant.objects.create(
        company_name=req_body['company_name'],
        image=req_body['image'],
        phone_number=req_body['phone_number'],
        market=Market.objects.get(pk=req_body['market_id']),
        user=new_user
    )

    merchant.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key, "user_role": "merchant", "id": merchant.id})
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_consumer(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    consumer = Consumer.objects.create(
        image=req_body['image'],
        phone_number=req_body['phone_number'],
        user=new_user
    )

    consumer.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key, "user_role": "consumer", "id": consumer.id})
    return HttpResponse(data, content_type='application/json')