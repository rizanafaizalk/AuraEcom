from django import forms

class addressform(forms.Form):
    
    Address1 = forms.CharField()
    Address2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipcode = forms.CharField()
    save_info = forms.BooleanField(required=False)
    default = forms.BooleanField(required=False)
    use_default =forms.BooleanField(required=False)