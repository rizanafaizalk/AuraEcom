from django.db import models
from productapp.models import Product
from django.utils.text import slugify
from django.contrib.auth.models import User
from coupon.models import Offer



# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE, blank=True, null=True)
   
    def __str__(self):
        return str(self.user)
    
# Creating Model Of WishList
class WishList(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


