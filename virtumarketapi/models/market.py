from django.db import models

class Market(models.Model):

    name = models.CharField(max_length=50)
    zip_code = models.IntegerField()

    class Meta:
        verbose_name = ("market")
        verbose_name_plural = ("markets")

    def __str__(self):
        return self.name
