from django.shortcuts import render, redirect,HttpResponseRedirect
# from django.views import View
from .models import Address
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

from django.contrib.auth.decorators import login_required

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
    address.save_info=False
    address.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def profile(request):
    if request.user:
        context = { 'address' : Address.objects.filter(user=request.user)
                  }
        return render(request, 'UserTemp/profile.html',context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

       


def update_address(request,adrs_id):
  address = Address.objects.get(id = adrs_id)

  if request.method == 'POST':
    new_name =request.POST.get('fullname')
    new_mobile =request.POST.get('mobile')
    new_house = request.POST.get('house1')
    new_city = request.POST.get('city1')
    new_state = request.POST.get('state1')
    new_zip = request.POST.get('zip1')
    if new_name:
      address.firstname = new_name
    if new_mobile:
      address.mobilenumber = new_mobile
    if new_house:
      address.Address1=  new_house
    if new_city:
      address.city = new_city
    if new_state:
      address.state = new_state
    if new_zip:
      address.zipcode = new_zip
   
    address.save()
    return redirect('profile')
  

def editprofile(request):
    user =request.user
    if request.method == 'POST':
            image = request.FILES.get('image')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            mobilenumber = request.POST.get('mobile_number')
            email = request.POST.get('email')

            if firstname:
                user.first_name = firstname
            if lastname:
                user.last_name = lastname
            if mobilenumber:
                user.phone = mobilenumber
            if email:
                user.email = email
            if image:
                user.image = image
            user.save()
            return redirect('profile')


# Change password
def change_password(request):
  if request.method == 'POST':
    current_password = request.POST.get('password')
    change_psw = request.POST.get('newpassword')
    comfirm_psw = request.POST.get('renewpassword')
    password_validate = ValidatePassword(change_psw)
        
    user = authenticate(username=request.user, password=current_password)
    if change_psw !=comfirm_psw:
      messages.error(request,"password dosen't Match")
      return redirect('change_password')
    
    if  change_psw == comfirm_psw :
        if password_validate is False:  
            messages.info(request,'Enter Strong Password')
            return redirect('change_password')

    if user is not None:
      user.set_password(change_psw)
      user.save()
      messages.error(request,"password change succesfully, please Login..!!")
      return redirect('login')

    else:
        messages.success(request,"Please enter your correct password")    
        return redirect('change_password')  
 
  return redirect('profile')


def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
  
 
