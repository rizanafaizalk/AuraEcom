from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from productapp.models import Product
from cartapp.models import Cart
from .models import WishList



def cart(request):
    cartdisplay = Cart.objects.filter(user=request.user)
    sub_total = 0
    min_shopin_price = 4000
    shipping_charge=500
    for item in cartdisplay:
        if item.product.offer:
            sub_total += item.product.discounted_price
        else:
            sub_total += item.product.price
    grand_total = sub_total
        
   

    context = {
        'cartitems' : cartdisplay,
        'sub_total': sub_total,
        'grand_total':grand_total,
        'shipping_charge' : shipping_charge,
        'min_shopin_price':min_shopin_price
    }
    return render(request,'UserTemp/shoppingCart.html',context)



# Create your views here.
def addtocart(request):
    if request.method == 'POST':
        print("hai")
        if request.user.is_authenticated:
            prodct_id = int(request.POST.get('product_id'))
            print(prodct_id,"anzil")
            prodct_check = Product.objects.filter(id=prodct_id)
            print(prodct_check,"daxo")
            if(prodct_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prodct_id)):
                    return JsonResponse({'status':"Product Aready in Cart"})
                else:
                    prodct_qntity = int(request.POST.get('product_qntty'))

                    # if prodct_check.product_quantity >= prodct_qntity:
                    Cart.objects.create(user=request.user, product_id=prodct_id, product_quantity=prodct_qntity)
                    return JsonResponse({'status':"Product added Successfully"})
                        # return redirect('shoppingCart')
                    # else:
                    #     return JsonResponse({'status':"Only" + str(prodct_check.product_quantity) + "quantity available"})

            else:
                return JsonResponse({'status':"No such Product Found"})

        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('ShoppingCart')

@login_required(login_url='login')
def wishList(request):
    wishlist = WishList.objects.filter(user=request.user)
    context = { 'wishlist' : wishlist }

    return render(request,'UserTemp/wishlist.html',context) 

def addToWishlist(request):
    if request.method == 'POST':
        print("Done wishlist by me")
        if request.user.is_authenticated:
            prodct_id = int(request.POST.get('product_id'))
            print(prodct_id,"anzil")
            prodct_check = Product.objects.filter(id=prodct_id)
            print(prodct_check,"daxo")
            if(prodct_check):
                if(WishList .objects.filter(user=request.user.id, product_id=prodct_id)):
                    return JsonResponse({'status':"Product Aready in WishList"})
                else:
                    WishList.objects.create(user=request.user, product_id=prodct_id)
                    return JsonResponse({'status':"Product added to WishList"})
                        # return redirect('shoppingCart')
                    # else:
                    #     return JsonResponse({'status':"Only" + str(prodct_check.product_quantity) + "quantity available"})

            else:
                return JsonResponse({'status':"No such Product Found"})

        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('/')


def DeleteWishlistItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prodct_id = int(request.POST.get('product_id'))
            print(prodct_id,"yes boi")
            if(WishList .objects.filter(user=request.user.id, product_id=prodct_id)):
                    wishlistitem =WishList.objects.get(product_id = prodct_id) 
                    wishlistitem.delete()
                    return JsonResponse({'status':"Product removed form wishlist"})
            else:
                    return JsonResponse({'status':"Product not found"})
                  
        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('/')

  
        