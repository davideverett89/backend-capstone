from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Consumer(models.Model):

    image = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("consumer")
        verbose_name_plural = ("consumers")
        ordering = (F('user.date_joined').asc(nulls_last=True),)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
