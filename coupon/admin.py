from django.contrib import admin
from coupon.models import coupon
from coupon.models import Offer

# Register your models here.
admin.site.register(coupon)
admin.site.register(Offer)

