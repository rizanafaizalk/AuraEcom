from django.contrib import admin
from .models import Address
from login.models import Account
# Register your models here.


admin.site.register(Address)
admin.site.register(Account)