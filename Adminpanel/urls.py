from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home, name="dashboardAdmin"),
    path('',views.dashboard, name="dashboard"),
    path('product',views.product, name="product"),
    path('orders',views.orders, name="orders"),
    path('users',views.users, name="users"),
    path('blockuser',views.blockuser, name="blockuser"),
    path('category',views.category, name="category"),
    path('addcategory',views.addcategory, name="addcategory"),
    path('brand',views.brand, name="brand"),
    path('addbrand',views.addbrand, name="addbrand"),
    path('coupon',views.Coupon, name="coupon"),
    path('addcoupon',views.addcoupon, name="addcoupon"),
    path('offer',views.offer, name="offer"),
    path('addOffer',views.addOffer, name="addOffer"),
    path('deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),
    path('editproduct/<int:prod_id>',views.editproduct,name='editproduct'),
    path('orderdelete/<int:id>',views.orderdelete,name='orderdelete'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('update_status/<int:order_item_id>',views.update_status,name ='update_status'),


]