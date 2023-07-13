from django.contrib.auth.forms import UserCreationForm

from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    class meta:
        model = User
        field = ['username','email','password1','password2']