from django.urls import path
from cartapp import views as addtocartview
from login import views as loginview
from . import views

urlpatterns = [
    path('',views.Userhome, name="Userhome"),
    path('usershop/',views.UserShop, name="UserShop"),
    path('product_search/',views.product_search, name="product_search"),
    path('filter_category/<int:cat>',views.filter_category, name="filter_category"),
    path('filter_brand/<int:brnd>',views.filter_brand, name="filter_brand"),
    path('filter_price/<int:prce>',views.filter_price, name="filter_price"),
    path('productdetail/<int:prdetails_id>',views.productdetail, name="productdetail"),
    # path('ShoppingCart/',views.ShoppingCart, name="ShoppingCart"),

    

    path('Checkout/',views.Checkout, name="Checkout"),
    

    

    
    
]