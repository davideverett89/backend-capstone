"""virtumarketapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from virtumarketapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"markets", Markets, "market")
router.register(r"goods", Goods, "good")
router.register(r"merchants", Merchants, "merchant")
router.register(r"good_types", GoodTypes, "good_type")
router.register(r"unit_sizes", UnitSizes, "unit_size")
router.register(r"users", Users, "user")


urlpatterns = [
    path('', include(router.urls)),
    path('register/merchant', register_merchant),
    path('register/consumer', register_consumer),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
