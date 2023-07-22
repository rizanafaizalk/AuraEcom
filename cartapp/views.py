from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from productapp.models import Product
from cartapp.models import Cart
from .models import WishList


@login_required(login_url='login')
def cart(request):
    cartdisplay = Cart.objects.filter(user=request.user)
    sub_total = 0
    min_shopin_price =5000
    for item in cartdisplay:
        sub_total += item.total
        
    grand_total = sub_total

    if grand_total<min_shopin_price and grand_total>0:
         shipping_charge=500
         grand_total += shipping_charge

    else:
        shipping_charge=0
        grand_total += shipping_charge

    context = {
        'cartitems' : cartdisplay,
        'sub_total': sub_total,
        'grand_total':grand_total,
        'shipping_charge' : shipping_charge,
        # 'shipping_charge_o':shipping_charge_o
    }
    return render(request,'UserTemp/shoppingCart.html',context)



# Create your views here.
def addtocart(request):
    if request.method == 'POST':
    
        if request.user.is_authenticated:
            prodct_id = int(request.POST.get('product_id'))
            prodct_check = Product.objects.filter(id=prodct_id).first()
            
            if(prodct_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prodct_id)):
                    return JsonResponse({'status':"Product Aready in Cart"})
                else:
                    prodct_qntity = int(request.POST.get('product_qntty'))

                    if prodct_check.offer:
                        tot =prodct_qntity*prodct_check.offer_price()
                    else:
                        tot=prodct_qntity*prodct_check.price    
                    # if prodct_check.product_quantity >= prodct_qntity:
                    Cart.objects.create(user=request.user, product_id=prodct_id, product_quantity=prodct_qntity,total= tot)
                    return JsonResponse({'status':"Product added Successfully"})
                        # return redirect('shoppingCart')
                    # else:
                    #     return JsonResponse({'status':"Only" + str(prodct_check.product_quantity) + "quantity available"})

            else:
                return JsonResponse({'status':"No such Product Found"})

        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('ShoppingCart')
#To DELETE CART items
def DeleteCartItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prodct_id = int(request.POST.get('product_id'))
            print(prodct_id,"yes Delete Cart boi")
            
            cartitem =Cart.objects.get(id = prodct_id) 
            print(cartitem.product.product_name,"ProoooooooooooooodddddddddddddduccccccccccccccttttttttNAME")
            cartitem.delete()
            return JsonResponse({'status':"Product removed form Cart"})
    
                  
        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('/')


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
            print(prodct_id,"yes boiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            wishlistitem =WishList.objects.get(id = prodct_id) 
            print(wishlistitem,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            wishlistitem.delete()
            return JsonResponse({'status':"Product removed form wishlist"})
    
                  
        else:
            return JsonResponse({'status':"Login to Continue"})
    
    return redirect('/')

def add_to_cart(request, wishlist_item_id):
    try:
        # Get the Wishlist item based on the provided ID
        wishlist_item = WishList.objects.get(id=wishlist_item_id)

        # Check if the Wishlist item is already in the Cart
        if Cart.objects.filter(product=wishlist_item.product, user=request.user).exists():
            # If it's already in the Cart, you may choose to show a message or handle it as per your requirements.
            pass
        else:
            # If the Wishlist item is not in the Cart, move it to the Cart
            Cart.objects.create(product=wishlist_item.product, user=request.user)

        # Remove the Wishlist item after adding it to the Cart
        wishlist_item.delete()

    except WishList.DoesNotExist:
        # Handle the case when the Wishlist item with the provided ID does not exist
        pass

    # Redirect the user back to the Wishlist page or any other desired page
    return redirect('wishList')  # Replace 'wishlist' with the URL name of your Wishlist page



def increase_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
       
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product.offer:
        price = int( cart_item.product.offer_price())
    
    if cart_item.product_quantity == cart_item.product.product_quantity:
        messages.error(request, 'Maximum quantity reached..!!')
        return JsonResponse({'message': 'Maximum quantity reached..!!',})
    else:
        cart_item.product_quantity+=1
        cart_item.total += price
        cart_item.save()
        return JsonResponse({'message': 'Quantity increased..',})
    
    
 

def decrease_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
    
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product.offer:
        price = int( cart_item.product.offer_price())
    if cart_item.product_quantity == 1:
        cart_item.delete()
        return JsonResponse({'message': 'Item removed',})
    else:
        cart_item.total -= price
        cart_item.product_quantity-=1
        cart_item.save()
        return JsonResponse({'message': 'Quantity decreased..',})    


  
        