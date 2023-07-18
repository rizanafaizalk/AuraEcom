from django.shortcuts import render
from order.models import Order
from userprofile.models import Address
from cartapp.models import Cart

from productapp.models import Product
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator


# Create your views here.

# Home
def Userhome(request):
    context = {}
    return render(request, 'UserTemp/index.html')

def UserShop(request):
    product = Product.objects.all()
    paginator = Paginator(product,6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)

    context = {
        'products' : paged_product
    }
    return render(request, 'UserTemp/shop.html',context)



def productdetail(request,prdetails_id):
    try:
        product = Product.objects.get(id=prdetails_id)
        # try:
        #     p = Cart.objects.get(user=request.user, product_id = prdetails_id)
        # except:
        #     p = None
        # if p:
        #     qnty = p.product_quantity
        # else:
        #     p=0

    except Exception as e:
        raise 
    context = {
        'product' : product,
        # 'qnty' : qnty
    }
    return render(request, 'UserTemp/productdetail.html',context)

# def profulldetails(request,id_profdet):
#     try:
#         fulldetls = Product.objects.get(id=id_profdet)
#     except Exception as e:
#         raise
#     context = {
#         'profdetls' : fulldetls
#     }
#     return render(request, 'UserTemp/productdetail.html',context)

# def ShoppingCart(request):
#     context = {}
#     return render(request, 'UserTemp/shoppingCart.html')

@login_required(login_url='login')
def Checkout(request):
    cartdisplay = Cart.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user)
   
    
    sub_total = 0
    shipping_charge = 0
    
    for item in cartdisplay:
        sub_total += item.total
        
    grand_total = sub_total

    if grand_total<5000:
         shipping_charge=500
         grand_total+= shipping_charge

    context = {
        'cartitems' : cartdisplay,
        'sub_total': sub_total,
        'grand_total':grand_total,
        'shipping_charge' : shipping_charge,
        'address' : address,
    }
    
    return render(request,'UserTemp/checkout.html',context)



