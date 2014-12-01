from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Phone(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16) # validators should be a list

class KegUser(models.Model):
    user = models.OneToOneField(User)
    phone_number = Phone()
    stripe_id = models.CharField(max_length=50)

class KegUserForm(ModelForm):
    class Meta:
        model = KegUser
        exclude = ['user']

class UserForm(ModelForm):
    class Meta:
        model = User

