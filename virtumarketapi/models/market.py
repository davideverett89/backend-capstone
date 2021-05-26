from django.db import models

class Market(models.Model):

    name = models.TextField()
    image = models.TextField(default="")
    description = models.TextField(default="")
    zip_code = models.IntegerField()

    class Meta:
        verbose_name = ("market")
        verbose_name_plural = ("markets")

    def __str__(self):
        return self.name
