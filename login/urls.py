from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('signup/',views.register,name="signup"),
    path('logout/',views.logout,name="logout"),

    path('forgot/',views.forgot,name="forgot"),
]
 
