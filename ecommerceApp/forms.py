from django.core.exceptions import ValidationError
from django import forms
from .models import Order, Customer,Product
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
    
class ProductForm(forms.ModelForm):
    
    more_images = forms.FileField(required=False,widget=forms.FileInput(attrs={
        "class":"form-control",
        "multiple":True,
        "placeholder ": "Upload others images",
    }))
    
    class Meta :
        model = Product 
        fields = ('title','slug','category','description','image', 'marked_price','selling_price','warranty','return_policy',)   
        
        widgets ={
            'title' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Entrer le titre ..."
            }),
            
            'slug' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Entrer le nom Unique ..."
            }),
            'category' : forms.Select(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Entrer le titre ..."
            }),
            
            'marked_price' : forms.NumberInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Entrer le prix d'Achat ..."
            }),
            
              'selling_price' : forms.NumberInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Entrer le prix de vente ..."
            }),
            
             'description' : forms.Textarea(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Decrivez le produit ...",
                "rows":5,
            }),
             
            'image' : forms.ClearableFileInput(attrs={
                "class" : "form-control",
            }),
            'warranty' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Durée de Garantie..."
            }),
            
            'return_policy' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Evenement de retour..."
            }),
        }
     
   
    
   
    