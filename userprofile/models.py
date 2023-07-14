from django.db import models
from django.contrib.auth.models import User
# from django_countries.fields

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    save_info = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username