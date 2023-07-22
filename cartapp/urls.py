from django.urls import path
from . import views

urlpatterns = [
    path('addtocart/',views.addtocart,name="addtocart"),
    path('cart/',views.cart,name="cart"),
    path('DeleteCartItem/',views.DeleteCartItem,name="DeleteCartItem"),
    path('wishList/',views.wishList,name="wishList"),
    path('addToWishlist/',views.addToWishlist,name="addToWishlist"),
    path('DeleteWishlistItem/',views.DeleteWishlistItem,name="DeleteWishlistItem"),
    path('decrease_count/',views.decrease_count,name="decrease_count"),
    path('increase_count/',views.increase_count,name="increase_count"),

    

]
 