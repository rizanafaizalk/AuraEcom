from django.urls import path
from cartapp import views as addtocartview
from login import views as loginview
from . import views

urlpatterns = [
    path('',views.Userhome, name="Userhome"),
    path('usershop/',views.UserShop, name="UserShop"),
    path('productdetail/<int:prdetails_id>',views.productdetail, name="productdetail"),
    # path('ShoppingCart/',views.ShoppingCart, name="ShoppingCart"),

    

    path('Checkout/',views.Checkout, name="Checkout"),
    

    

    
    
]