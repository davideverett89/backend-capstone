from django.db import models
from .good import Good
from .basket import Basket

class GoodBasket(models.Model):

    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="current")
    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, related_name="current")
    date_added = models.DateField()

    class Meta:
        verbose_name = ("good_basket")
        verbose_name_plural = ("good_baskets")

    def __str__(self):
        return self.name
