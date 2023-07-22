from django.urls import path
from cartapp import views as addtocartview
from login import views as loginview
from . import views

urlpatterns = [
    path('placeorder/',views.placeorder, name="placeorder"),
    path('UserOrdersPage/',views.UserOrdersPage, name="UserOrdersPage"),
    path('SingleOrdersPage/<int:order_id>/',views.SingleOrdersPage, name="SingleOrdersPage"),
    path('cancel_order/<int:order_item_id>',views.cancel_order, name="cancel_order"),
    path('return_item/',views.return_item, name="return_item"),


    path('proceedtopay/',views.proceedtopay, name="proceedtopay"),
    path('print/',views.print, name="print"),

    

    
    
]