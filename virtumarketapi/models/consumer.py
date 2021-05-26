from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Consumer(models.Model):

    bio = models.TextField(default="")
    profile_image = models.TextField(default="")
    phone_number = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("consumer")
        verbose_name_plural = ("consumers")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
