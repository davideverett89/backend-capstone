from django.db import models
from .consumer import Consumer

class PaymentMethod(models.Model):

    merchant_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    expiration_date = models.DateField()
    creation_date = models.DateField()
    consumer = models.ForeignKey(Consumer, on_delete=models.DO_NOTHING, related_name="payment_methods")


    class Meta:
        verbose_name = ("payment_method")
        verbose_name_plural = ("payment_methods")

    def __str__(self):
        return self.name