from django.db import models
from .consumer import Consumer
from .payment_method import PaymentMethod

class Basket(models.Model):

    consumer = models.ForeignKey(Consumer, on_delete=models.DO_NOTHING, related_name="baskets")
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="baskets")
    date_completed = models.DateField(blank=True, null=True)
    goods = models.ManyToManyField("Good", through=("GoodBasket"))

    class Meta:
        verbose_name = ("basket")
        verbose_name_plural = ("baskets")

    def __str__(self):
        return self.name