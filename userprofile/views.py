from django.shortcuts import render, redirect
# from django.views import View
from .models import Address

from .forms import addressform

# Create your views here.
# class checkoutview(View):
#     def get(self, *args, **kwargs):
#         form = addressform()
#         context = {
#             'form' : form
#         }
#         return render(self.request, 'UserStatic/checkout.html', context)

def addAddress(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        Address1 = request.POST.get('Address1')
        Address2 = request.POST.get('Address2')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        state = request.POST.get('state')

        Address.objects.create(user=request.user,firstname=fname,lastname=lname,mobilenumber=phone,email=email,Address1=Address1,Address2=Address2,city=city,zipcode=zipcode,state=state)

    
        return redirect('Checkout')
    
def deleteaddress(request,address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    
    return redirect('Checkout')
