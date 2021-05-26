from django.db import models

class GoodType(models.Model):

    name = models.TextField()

    class Meta:
        verbose_name = ("goodType")
        verbose_name_plural = ("goodTypes")

    def __str__(self):
        return self.name
