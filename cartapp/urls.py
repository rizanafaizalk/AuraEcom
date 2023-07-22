from django.urls import path
from . import views

urlpatterns = [
    path('addtocart/',views.addtocart,name="addtocart"),
    path('cart/',views.cart,name="cart"),
    path('DeleteCartItem/',views.DeleteCartItem,name="DeleteCartItem"),
    path('wishList/',views.wishList,name="wishList"),
    path('addToWishlist/',views.addToWishlist,name="addToWishlist"),
    path('DeleteWishlistItem/',views.DeleteWishlistItem,name="DeleteWishlistItem"),
    

]
 