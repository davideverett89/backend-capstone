from django.db import models

class UnitSize(models.Model):

    name = models.TextField()

    class Meta:
        verbose_name = ("unitSize")
        verbose_name_plural = ("unitSizes")

    def __str__(self):
        return self.name