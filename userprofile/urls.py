
from django.urls import path
from . import views

urlpatterns = [
    path('addAddress/',views.addAddress,name="addAddress"),
    path('deleteaddress/<int:address_id>/',views.deleteaddress,name="deleteaddress"),

    path('profile/',views.profile,name="profile"),
    path('update_address/<int:adrs_id>/',views.update_address,name="update_address"),
    path('editprofile',views.editprofile,name="editprofile"),
    path('change_password',views.change_password,name="change_password"),
]
 
