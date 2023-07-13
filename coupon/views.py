from datetime import timezone
import decimal
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from userprofile.models import Address
from cartapp.models import Cart
from login.models import Account
from coupon.forms import CouponForm
from .models import coupon
# from login.views import coupon
from order.models import UsedCoupon

# Create your views here.
def add_coupon(request):
    if request.method == 'POST':
        released_date = timezone.now()
        couponform = CouponForm(request.POST)

        if couponform.is_valid():
            coupon = couponform.save(commit=False)
            coupon.released_date = released_date
            coupon.save()
            return redirect('coupon_management')
        else:
            print(couponform.errors,"coupon code not found error")
    else:
        couponform = CouponForm()
    
    return redirect('coupon_management')

def edit_coupon(request, coupon_id):
    try:
        coupon = coupon.objects.get(id=coupon_id)
    except:
        coupon = None
    
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_management')
        else:
            form = CouponForm(instance=coupon)
    return render(request, 'edit_coupon.html',{'form':form, 'coupon':coupon})

def coupon_management(request):
    list_coupon = coupon.objects.all()
    context = {
        'coupon' : list_coupon
    }
    return render(request,'create_coupon.html',context)

def apply_coupon(request):
    user_id = request.user
    print(user_id,"rizana")

    if request.method == 'POST':
        new_coupon=request.POST.get('coupon')
        coupon_exists=coupon.objects.filter(code=new_coupon)
        cartdisplay = Cart.objects.filter(user=request.user)
        shipping_charge = 40
        for i in cartdisplay:
            sub_total = i.product_quantity * i.product.price
        if coupon_exists:
            coupon_used = UsedCoupon.objects.filter(coupon_used=new_coupon, order__user = user_id).exists()
            if coupon_used:
                print("coupon already used")
                messages.error(request, 'Coupon already used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
            else:
                if user_id:
                    cart_items = Cart.objects.filter(user=user_id)
                    if cart_items:
                        grand_total = sum(item.product.price * item.product_quantity for item in cart_items)
                        shipping_price = 40
                        grand_total=grand_total+shipping_price
                        oupon = coupon_exists.get()
                        grand_total=grand_total-oupon.discount
                        
                    else:
                        messages.info(request,"Cart is Empty")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
                else:
                    cart_items = []
                    grand_total = 0
                user_address = Address.objects.filter(user=user_id)
                context = {
                    'user' :user_id,
                    'cart' :cart_items,
                    'address':user_address,
                    'coupon':coupon_exists,
                    'cartitems' : cartdisplay,
                    'sub_total': sub_total,
                    'grand_total':grand_total,
                    'shipping_charge' : shipping_charge,
                }
            return render(request, 'UserTemp/checkout.html', context)
        else:
            messages.error(request, 'Invalid coupon')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        