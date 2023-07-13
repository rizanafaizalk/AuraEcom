from ctypes import cast
from datetime import timedelta
import datetime
from django.contrib import messages
from django.db.models import DateField
from django.forms import DateField
from django.shortcuts import render,redirect
from cartapp.models import Cart
from django.db.models.functions import ExtractMonth
from productapp.models import Product
from order.models import Order, OrderItem
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models.functions import TruncDay
from coupon.models import Offer

from django.db.models import Sum

from category.models import Category,Brand
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'AdminDashboard/home.html')

# def dashboard(request):

#    return render(request, 'AdminDashboard/dashboard.html')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('signin')

    delivered_items = OrderItem.objects.filter(status='Order Confirmed')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price
    print(revenue)
    top_selling = OrderItem.objects.annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.date.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    orders = Order.objects.filter( created_at__gte=four_days_ago, created_at__lte=today)

    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')

    # sales_dates = Order.objects.annotate(sale_date= cast('created_at', output_field = DateField())).values('sale_date').distinct()

    context = {
        'total_users':User.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,  
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    
    return render(request, 'AdminDashboard/dashboard.html',context)

def product(request):
    userproduct=Product.objects.all()
    context = {
        'userproducts': userproduct

    }
    return render(request, 'AdminDashboard/product.html',context)

def addproduct(request):
    if request.method == 'POST':
        name= request.POST['product_name']
        image1= request.FILES.get('image1')
        image2= request.FILES.get('image2')
        image3= request.FILES.get('image3')
        image4= request.FILES.get('image4')
        qty=request.POST['quantity']
        price = request.POST['product_price']
        description=request.POST['product_description']
        offer_id = request.POST.get('offer')
        productDetails=request.POST['product_details']
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        brand_id = request.POST.get('brand')
        brand = Brand.objects.get(id=brand_id)
        
        try:
            offer = Offer.objects.get(id=offer_id)
        except:
            offer = None    
        # Validaiton
        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'Product name already exists')
            return redirect('addproduct')
            
        if name == "or price ==":
            messages.error(request,'Name or Price field are empty')
            return redirect('product')
        if not (image1,image2,image3,image4):
            messages.error(request,'Image not uploaded')
            return redirect('product')
        
        #Save
        product =Product(   product_name =name,
                         product_image=image1,
                         product_image1=image2,
                         product_image2=image3,
                         product_image3=image4,
                        product_quantity =qty,
                        price = price,
                        offer= offer,
                        description = description,
                        prodetails = productDetails,
                        brand = brand,
                        category= category )
        product.save()
        messages.success(request, 'Product added successfully') #for notifying
        return redirect('product')
    context = {
                'category' : Category.objects.all(),
                'brand' : Brand.objects.all(),
                'offers' : Offer.objects.all()
                }
    return render(request,'AdminDashboard/addProduct.html', context)



def deleteproduct(request,id):
    one=Product.objects.get(id=id)
    if one.is_active:
        one.is_active=False
        one.save()
        messages.success(request, 'Product Deleted successfully') #for notifying
        return redirect('product')
    else:
        one.is_active=True
        one.save()
        messages.success(request, 'Product Brought back successfully') #for notifying
        return redirect('product')    
    

def editproduct(request,prod_id):
    prd=Product.objects.get(id=prod_id)
    if request.method == 'POST':
        name= request.POST['product_name']
        image1= request.FILES.get('image1')
        image2= request.FILES.get('image2')
        image3= request.FILES.get('image3')
        image4= request.FILES.get('image4')
        qty=request.POST['quantity']
        price = request.POST['product_price']
        description=request.POST['product_description']
        offer_id = request.POST.get('offer')
        productDetails=request.POST['product_details']
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        category = Category.objects.get(id=category_id)
        brand_name = Brand.objects.get(id = brand_id)

        try:
            offer = Offer.objects.get(id=offer_id)
        except:
            offer = None   
        
        if name == ""or price =="":
            messages.error(request,'Name or Price field are empty')
            return redirect('product')
        if not (image1,image2,image3,image4):
            messages.error(request,'Image not uploaded')
            return redirect('product')
        print(brand_name,'daxoooooooooo')
        # Validaiton
        # if Product.objects.filter(product_name=name).exclude(id=prod_id).exists():
        #     messages.error(request,'Product name already exists')
        #     return redirect('addproduct')
        #Save

        prduct=Product.objects.get(id=prod_id)
        prduct.product_name =name
        prduct.product_image=image1
        prduct.product_image1=image2
        prduct.product_image2=image3
        prduct.product_image3=image4
        prduct.product_quantity =qty
        prduct.price = price
        prduct.description = description
        prduct.offer = offer
        prduct.prodetails = productDetails
        prduct.brand = brand_name
        prduct.category= category 
        prduct.save()

        print(prd,"iiiiiiiiiiiiiiiii")
        messages.success(request, 'Product Editted successfully') #for notifying
        return redirect('product')
    context = {
                'category' : Category.objects.all(),
                'brand' : Brand.objects.all(),

                 'product' : prd,
                 'offer' :Offer.objects.all()
                }
    

    return render(request, 'AdminDashboard/editProduct.html',context)

def orderdelete(requesti,id):
    delorder = OrderItem.objects.get(id=id)
    delorder.delete()
    return redirect('orders')

def orders(request):
    orderitemslist = OrderItem.objects.all()
    context = {
        'OrderitemList' : orderitemslist

    }
    return render(request,'AdminDashboard/orders.html', context)

def users(request):
    context = {}
    return render(request, 'AdminDashboard/users.html')

def offer(request):
    if request.method == 'POST':
        offr_id = request.POST.get('offer_id')
        offr_name =  request.POST.get('name')
        discount =  request.POST.get('discount')
        start_date =  request.POST.get('start_date')
        end_date =  request.POST.get('end_date')
        
        offer = Offer.objects.get(id=offr_id)
       
        if offr_name:
            offer.name =offr_name
        if discount:
            offer.discount =discount
        if start_date:
            offer.start_date =start_date   
        if end_date:
            offer.end_date =end_date
            
        offer.save()
        messages.success(request,'Offer Updated')
        return redirect('offer')
    context = {'offer': Offer.objects.all()}
    return render(request, 'AdminDashboard/offer.html',context)

def addOffer(request):
    if request.method == 'POST':
        offername= request.POST.get('name')
        discount = request.POST.get('discount')
        start_date=request.POST.get('start_date')        
        end_date=request.POST.get('end_date')

        if not start_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offers_list')
        if not end_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offer')
            
        if offername:
            offername= offername.strip()
            exist = Offer.objects.filter(name= offername)
            if exist:
                messages.success(request, 'Offer name already exist..!')
                return redirect('offer')
            if discount: 
                Offer.objects.create(name=offername, discount= discount, start_date= start_date, end_date= end_date)
                return redirect('offer') 
            else:
                messages.success(request, 'Please Specify a discount..!')
                return redirect('offer')  
                    
        else:
            messages.success(request, 'Offer should have a name..!')
            return redirect('offer')
    context = {'offer': Offer.objects.all()}
    return render(request, 'AdminDashboard/offer.html',context)

def update_status(request, order_item_id):
    if not request.user.is_superuser:
        return redirect('signin')
    order_item = OrderItem.objects.get(id=order_item_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        order_item.status = status
        order_item.save()
        return redirect('orders')


