from django.db import models
from category.models import Category,Brand
from django.utils.text import slugify
from coupon.models import Offer


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='photos/product')
    product_image1= models.ImageField(upload_to='photos/product',null=True)
    product_image2= models.ImageField(upload_to='photos/product',null=True)
    product_image3= models.ImageField(upload_to='photos/product',null=True)
    product_quantity = models.IntegerField()
    price = models.IntegerField()
    description = models.CharField(max_length=250, default='Newly Arrived')
    prodetails = models.CharField(max_length=250, default='Full des')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE, blank=True, null=True)
    discounted_price = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def offer_price(self):
        offer = self.offer
        if offer:
            discount_percentage = offer.discount
            new_price = self.price - (self.price * discount_percentage / 100)
            self.discounted_price = new_price
            self.save()
            return self.discounted_price

    def save(self, *args, **kwargs):
    # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name
    
