from django.db import models
from .good_type import GoodType
from .unit_size import UnitSize
from .merchant import Merchant
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Good(SafeDeleteModel):

    name = models.TextField()
    image = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    quantity = models.IntegerField()
    good_type = models.ForeignKey(GoodType, on_delete=models.DO_NOTHING, related_name="good")
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, related_name="goods")
    unit_size = models.ForeignKey(UnitSize, on_delete=models.DO_NOTHING, related_name="good")
    on_order = models.BooleanField(default=False)
    _safedelete_policy = SOFT_DELETE

    class Meta:
        verbose_name = ("good")
        verbose_name_plural = ("goods")

    def __str__(self):
        return self.name