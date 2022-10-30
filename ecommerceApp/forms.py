from dataclasses import fields
from django.core.exceptions import ValidationError
from django import forms
from .models import Order, Customer
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    
    class Meta :
        model = Order 
        fields = ['ordered_by','shipping_adress','mobile','email','order_status']
    

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=200,widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email =  forms.CharField(widget=forms.TextInput())
    
    class Meta :
        model = Customer
        fields = ["username","password","email","full_name","telephone","adresse"]
    
    def clean_username(self) :
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'This user alredy exists !!'
            )
        return username
    

class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=200,widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
   
    
   
    