from django import forms

from coupon.models import coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = coupon
        fields = ['code','discount','is_expired','min_price']

