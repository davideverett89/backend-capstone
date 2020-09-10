from django.db import models

class UnitSize(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("unitSize")
        verbose_name_plural = ("unitSizes")

    def __str__(self):
        return self.name