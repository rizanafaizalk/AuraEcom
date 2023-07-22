from django.db import models
from django.contrib.auth.models import User
from userprofile.models import Address
from productapp.models import Product
from coupon.models import coupon

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null= False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(coupon,on_delete=models.CASCADE,blank=True,null=True)
    


    def _str_(self):
        return self.tracking_no
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(max_length=150,choices=STATUS, default='Pending')
    total = models.BigIntegerField(null=True, blank=True)

    def str(self):
        return '() ()'.format(self.order.id, self.order.tracking_no)
    
class UsedCoupon(models.Model):
    coupon_used = models.CharField(max_length=50,unique=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,blank=True,null=True)


class Returned(models.Model):
    returned_product =  models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)  
    reason           =   models.CharField(max_length=50, blank=True,null=True)
    comments         =  models.CharField(max_length=250, blank=True,null=True)    