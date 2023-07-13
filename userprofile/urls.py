
from django.urls import path
from . import views

urlpatterns = [
    path('addAddress/',views.addAddress,name="addAddress"),
    path('deleteaddress/<int:address_id>/',views.deleteaddress,name="deleteaddress"),
]
 
