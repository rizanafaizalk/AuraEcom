from django.db import models

# Create your models here.
class coupon(models.Model):
    released_date = models.DateTimeField(auto_now_add=True,null=True)
    code = models.CharField(max_length=50,unique=True)
    discount = models.DecimalField(max_digits=8,decimal_places=2)
    is_expired = models.BooleanField(default=False)
    min_price = models.DecimalField(max_digits=10,decimal_places=2)


class Offer(models.Model):
    name = models.CharField(max_length=30,unique=True)
    discount = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    