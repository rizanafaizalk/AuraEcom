from django.db import models
from django.utils.text import slugify

# Create your models here.

#Brand
class Brand(models.Model):
    name = models.CharField(max_length=200)
    brand_address = models.TextField(max_length=200)
    discription = models.TextField(max_length=200)
    slug = models.SlugField(max_length=250,unique=True)

    def save(self, *args, **kwargs):
    # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self) :
        return self.name
    
#Category
class  Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    category_discription = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250,unique=True)

    def save(self, *args, **kwargs):
    # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.category_name



