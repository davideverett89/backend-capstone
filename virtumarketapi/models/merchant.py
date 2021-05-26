from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from .market import Market

class Merchant(models.Model):
    """Class that defines the Merchants model."""

    company_name = models.TextField()
    bio = models.TextField(default="")
    profile_image = models.TextField(default="")
    booth_image = models.TextField(default="")
    phone_number = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant")
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="merchants")


    class Meta:
        verbose_name = ("merchant")
        verbose_name_plural = ("merchants")
        ordering = (F('company_name').asc(nulls_last=True),)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
