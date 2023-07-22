import random
from django.shortcuts import redirect, render

from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

from productapp.models import Product
from .models import Order, Returned
from .models import OrderItem
from cartapp.models import Cart
from userprofile.models import Address
from storeapp.views import Checkout

from django.shortcuts import get_object_or_404


# Create your views here.
def placeorder(request):
   
    if request.method == 'POST':

        # coupon_code = request.POST['coupon']
        
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST.get('address')
        if address_id:
            address = Address.objects.get(id=address_id)
        else:
            messages.error(request,'Please select an Address..!!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        neworder.address = address
        neworder.payment_mode = request.POST.get('payment')
        
        neworder.payment_id = request.POST.get('payment_id')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            # if item.product.offer:

            #     cart_total_price = item.product.get_offer_price() * item.quantity

            # else:
                cart_total_price += item.total
            # item.product.stock-=item.quantity
        tax = (2*cart_total_price)/100
        neworder.total_price = cart_total_price + tax
        if cart_total_price<5000:
            neworder.total_price += 500

        trackno = random.randint(1111111, 9999999)

        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()

        # try:
        #     instance = UserCoupon.objects.get(user=request.user)

        #     if float(cart_total_price) >= float(instance.coupon.min_value):
        #         coupon_discount = (
        #             (float(cart_total_price) * float(instance.coupon.discount))/100)
        #         cart_total_price = float(cart_total_price) - coupon_discount
        #         cart_total_price = format(cart_total_price, '.2f')
        #         coupon_discount = format(coupon_discount, '.2f')

        #     instance.delete()
        #     neworder.total_price = cart_total_price
        #     neworder.save()

        # except:
        #     pass


        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            if item.product.offer:
                tot = item.product.offer_price()
            else:
                tot = item.product.price    

            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=tot,
                quantity=item.product_quantity,
                total = tot*item.product_quantity
                
            )

            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.product_quantity = orderproduct.product_quantity - item.product_quantity
            orderproduct.save()
            # payment_mode = request.POST.get('payment_method')

            payment_mode = request.POST.get('payment') 
            if payment_mode == 'Razorpay':
                Cart.objects.filter(user=request.user).delete()
                return JsonResponse({'status' : "Your order has been succesfully placed"})

        # To clear user Cart
        Cart.objects.filter(user=request.user).delete()
        

        context={
            'order' : OrderItem.objects.filter(order=neworder),
        }

    messages.error(request,'Order Placed..!!')
    return redirect('UserOrdersPage')

@login_required(login_url='login')
def UserOrdersPage(request):
    orderlist=Order.objects.filter(user=request.user).order_by('-created_at')
    # order = Order.objects.filter(user=request.user)
    context = {
        'orderlist' : orderlist,
        # 'order_id': order.tracking_no, 

    }
    return render(request,'UserTemp/ordersPage.html',context)

def SingleOrdersPage(request,order_id):
    order = Order.objects.get(id=order_id)
    singleOrderList = OrderItem.objects.filter(order = order_id)
    context = {
        'singleOrderList' : singleOrderList,
        'order' :order,
    }
    
    return render(request,'UserTemp/singleOrderPage.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def cancel_order(request,order_item_id):
   customer = request.user
   ord_prod = OrderItem.objects.get(id=order_item_id)

   ord_prod.status = 'Cancelled' 
   if ord_prod.order.payment_mode != "cod":
        customer.wallet = customer.wallet + ord_prod.total
   ord_prod.product.product_quantity += ord_prod.quantity
   ord_prod.order.total_price -= ord_prod.total
   ord_prod.order.save()
   ord_prod.product.save()
   ord_prod.save()
   customer.save()


   messages.error(request,'Order Cancelled..!!')
   if ord_prod.order.payment_mode != "cod":
        messages.error(request,'Amount Refunded to your Wallet..!!')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def return_item(request):
    if request.method == 'POST':
        ord_id = request.POST.get('item')
        reason = request.POST.get('return_reason')
        note = request.POST.get('return_comment')
        
        return_product = OrderItem.objects.get(id=ord_id)
        Returned.objects.create(returned_product = return_product, reason = reason, comments = note)
        
        return_product.status = 'Returned'
    
        request.user.wallet += return_product.total
        
        return_product.save()
        request.user.save()
        
        if reason == 'Ordered by mistake' or reason == 'Wrong item':
            return_product.product.product_quantity += return_product.quantity
            return_product.product.save()
        
        
        messages.error(request,'Item return initiated, will be processed in 2 days, please see the amount in your Wallet..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def proceedtopay(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    shipping_charge = 40
    for item in cart:
        total_price = total_price + item.product.price * item.product_quantity 
        grand_total = total_price +shipping_charge

    return JsonResponse({
         'grand_total' : grand_total
    })


