import queue
from django.shortcuts import render
from order.models import Order
from userprofile.models import Address
from cartapp.models import Cart
from category.models import Brand,Category

from productapp.models import Product
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages

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
        'brands' : Brand.objects.all(),
        'category' : Category.objects.all(),
        'products' : paged_product
    }
    return render(request, 'UserTemp/shop.html',context)

# Product Search
def product_search(request):
    key = request.GET.get('key')
    print('hai key')
    context = {
             'category': Category.objects.all(),
            'products':Product.objects.filter(Q(brand__name__icontains=key) |Q(product_name__icontains=key) | Q(description__icontains=key) | Q(category__category_name__icontains=key) | Q(discounted_price__icontains=key)),
            'brands' : Brand.objects.all()
        }
    print(key,'hai key')
    messages.error(request,"Products matching : "+key)
    return render(request,"UserTemp/shop.html",context)
# filter by  Category
def filter_category(request, cat):
    key = Category.objects.get(id=cat)
    print('hai cate')
    context = {
            'category': Category.objects.all().order_by('id'),
            'brands' : Brand.objects.all(),
            'products': Product.objects.filter(category=key)

            
        }
    print(key,'hai key')
    messages.error(request,"Products matching Category: "+key.category_name)
    return render(request,"UserTemp/shop.html",context)
# filter by  Brand
def filter_brand(request, brnd):
    key = Brand.objects.get(id=brnd)
    context = {
            'category': Category.objects.all(),
            'brands' : Brand.objects.all().order_by('id'),
            'products': Product.objects.filter(brand=key)

            
        }
    messages.error(request,"Products matching Brand: "+key.name)
    return render(request,"UserTemp/shop.html",context)
# filter by  Price
def filter_price(request, prce):
    key = Product.objects.get(id=prce)
    context = {
            'category': Category.objects.all(),
            'brands' : Brand.objects.all().order_by('id'),
            'products': Product.objects.filter(brand=key)

            
        }
    messages.error(request,"Products matching Brand: "+key.price)
    return render(request,"UserTemp/shop.html",context)




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



