from django.db import models
from django.core.validators import RegexValidator
"""
class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True) # validators should be a list

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    phone = Phone()
    stripe = models.CharField(max_length=50)
    

    def __unicode__(self):              
        return self.name + ": " + self.email
"""
class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True) # validators should be a list

class KegUser(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	phone_number = Phone()
	stripe_key = models.CharField(max_length=100)
