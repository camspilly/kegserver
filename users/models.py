from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    pin = models.IntegerField(default=0)
    stripe = models.CharField(max_length=50)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name + ": " + self.email
