from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class myaccountDetails(BaseUserManager):
    def create_user(self,fname,lname,username,email,password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username ")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            fname = fname,
            lname = lname,

        )
        user.set_password(password)
        user.save(using = self._db) #._db?
        return user
    
    #superuser
    def creste_superuser(self,fname,lname,username,email,password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            fname = fname,
            lname = lname,
            )
        user.is_admin = True

# Create your models here.
class Account(AbstractBaseUser):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    user_image = models.ImageField(upload_to='photos/profile',blank=True,null=True,default='photos/profile/vk.high.png')

    #requiredFields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','fname','lname']

    objects = myaccountDetails()

    def __str__(self):
        return self.email
    
    def has_perm(self, prem, obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

class UserOTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()
