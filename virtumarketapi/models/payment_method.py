from django.db import models
from .consumer import Consumer
from safedelete.models import SafeDeleteModel, SOFT_DELETE

class PaymentMethod(SafeDeleteModel):

    merchant_name = models.TextField()
    account_number = models.TextField()
    expiration_date = models.DateField()
    creation_date = models.DateField()
    consumer = models.ForeignKey(Consumer, on_delete=models.DO_NOTHING, related_name="paymentmethods")
    _safedelete_policy = SOFT_DELETE



    class Meta:
        verbose_name = ("payment_method")
        verbose_name_plural = ("payment_methods")

    def __str__(self):
        return self.name