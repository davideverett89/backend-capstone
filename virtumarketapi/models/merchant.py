from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from .market import Market

class Merchant(models.Model):
    """Class that defines the Merchants model."""

    company_name = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="merchants")


    class Meta:
        verbose_name = ("merchant")
        verbose_name_plural = ("merchants")
        ordering = (F('company_name').asc(nulls_last=True),)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
