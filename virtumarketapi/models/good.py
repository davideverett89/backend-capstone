from django.db import models
from .good_type import GoodType
from .unit_size import UnitSize
from .merchant import Merchant

class Good(models.Model):

    name = models.CharField(max_length=50)
    image = models.CharField(max_length=500, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    good_type = models.ForeignKey(GoodType, on_delete=models.DO_NOTHING, related_name="good")
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, related_name="goods")
    unit_size = models.ForeignKey(UnitSize, on_delete=models.DO_NOTHING, related_name="good")
    number_on_order = models.IntegerField(blank=True, default=0)

    class Meta:
        verbose_name = ("good")
        verbose_name_plural = ("goods")

    def __str__(self):
        return self.name