from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class KegUser(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.PositiveIntegerField(max_length=15)
    stripe_id = models.CharField(max_length=50)

class KegUserForm(ModelForm):
    class Meta:
        model = KegUser
        exclude = ['user', 'stripe_id']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

