from multiprocessing import AuthenticationError
import random
import re
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from AuraEcom import settings
from login.models import Account, UserOTP


from login.forms import CustomUserForm

#login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
            return redirect('Userhome')

    if request.method=='POST':
        uname=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=uname.strip(),password=password)
        
        print(uname,password, user, "gggggggggggggggggggggggggggggggggggggggggg")
        #validation
        if uname.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('login')
        if user is not None:
            auth_login(request, user)
            return redirect('Userhome')
        else:
            messages.error(request, "Your username or password is Incorrect")
            return redirect('login')

    return render(request,"UserTemp/login.html")

#signupPage
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def signup(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         fname=request.POST.get('firstname')
#         lname=request.POST.get('lastname')
#         email=request.POST.get('email')
#         password1=request.POST.get('password1')
#         password2=request.POST.get('password2')

#         # print(uname,fname,lname,email,password1,password2)
# # Validation
#         if uname.strip() == '' or password1.strip() == '' or password2.strip() =='' or fname.strip() == '':
#             messages.error(request, "Fields can't be blank")
#             return redirect('signup')
        
#         if password1!=password2:
#             messages.error(request,"password dosen't Match")
#             return redirect('signup')
        
#         if User.objects.filter(username=uname).exists():
#             messages.error(request, 'Username already exists')
#             return redirect('signup')

#         my_user=User.objects.create_user(username=uname,first_name=fname,last_name=lname,email=email,password=password1)
#         my_user.save()
#         # return HttpResponse("User has been created sucessfully!!!!")
#         messages.success(request, 'User created successfully')
#         return redirect('login')


#     return render(request,"UserTemp/signup.html")

def validateEmail( email ):
    from django.core.validators import validate_email
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    else:
        return False

def register(request):

    """ OTP VERIFICATION """

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth_login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('Userhome')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'UserTemp/signup.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            firstname = request.POST.get('firstname') 
            lastname = request.POST.get('lastname')  
            username = request.POST.get('username')
            email = request.POST.get('email')
            # mobile = request.POST.get('mobile')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
             # null values checking
            check = [username,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'UserTemp/signup.html',context)
                
            try :
                uuser =User.objects.get(username=username)
                if uuser:
                        messages.info(request,'Username already taken, please try another')
                        return render(request,'UserTemp/signup.html',context)
            except:
                uuser =None

            result = validate_name(username)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request,'UserTemp/signup.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'UserTemp/signup.html',context)
            else:
                pass
                        
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request,'UserTemp/signup.html',context)
            else:
                pass
            if password1 == password2:
          
                try:
                    User.objects.get(email=email)
                except:
                    usr = User.objects.create_user(first_name=firstname, last_name=lastname, username=username,email=email,password=password1)
                    usr.is_active=False
                    usr.save()
                    
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for AuraEcom is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to AuraEcom Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    messages.info(request,'Enter the OTP that has been send to Your Email')
                    return render(request,'UserTemp/signup.html',{'otp':True,'usr':usr})
                    
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'user already exist')
                    return render(request,'UserTemp/signup.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':username,
                        'pre_email':email,
                        # 'pre_mobile':mobile,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'UserTemp/signup.html',context)
    else:
        return render(request,'UserTemp/signup.html')
    


def forgetpassword(request):
    if request.method == 'POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=Account.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                AuthenticationError.login(request,usr)
                messages.success(request,f'Now you can reset your password {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return render(request, 'user_view/resetpassword.html',{'user':usr})
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request, 'user_view/forgetpassword.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            email = request.POST.get('email')
            if Account.objects.filter(email=email).exists():
                usr = Account.objects.get(email__exact=email)
                user_otp=random.randint(1000,9999)
                UserOTP.objects.create(user=usr,otp=user_otp)
                mess=f'Hello\t{usr.username},\nYour OTP to forgot password is {user_otp}\nThanks!'
                send_mail(
                        "welcome to Beatandbase Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                messages.success(request, 'OTP sent to you email')
                return render(request, 'user_view/forgetpassword.html',{'otp':True,'usr':usr})

            else:
                messages.error(request, 'Account does not exist!')
                return redirect('forgot_password')
    return render(request, 'user_view/forgetpassword.html')


from django.core.exceptions import ValidationError

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

    
def resetpassword(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = request.POST.get('fjkha67UTAnh?"}[njkGTFCXD#A@!21^^*87ghjuguy67')
            user = Account.objects.get(id=user)
            Pass = ValidatePassword(password)
            if Pass is False:
                messages.success(request, 'Enter Strong password')
                message = 'Enter Strong password'
                return redirect('resetpassword')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset succesfull')
            return redirect('login_view')
        else:
            messages.error(request, 'Password doesnot match')
            return redirect('resetpassword')

    return render(request, 'user_view/resetpassword.html')

#logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('Userhome')

def forgot(request):

    return render(request, 'UserTemp/forgot.html')