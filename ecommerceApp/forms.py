from django.core.exceptions import ValidationError
from django import forms
from .models import Order, Customer,Product
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    
    class Meta :
        model = Order 
        fields = ['ordered_by','shipping_adress','mobile','email','order_status']
    

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex : SODYAM ..."
            }),label="Nom Utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "..."
            }),label="Mot de Passe")
    email =  forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex : exemple@gmail.com ..."
            }), label="L'adresse Email")
    
    class Meta :
        model = Customer
        fields = ["username","password","email","full_name","telephone","adresse"]

        widgets ={
            'full_name' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex : SODOKIN Yao Marius"
            }),
            'telephone' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex : +229 90500075"
            }),
            
             'adresse' : forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex :  Cotonou, Akpakpa"
            }),
        }
         
    def clean_username(self) :
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists() :
            raise ValidationError(
                'This user alredy exists !!'
            )
        return username
    

class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "Ex : SODYAM ..."
            }),label="Nom Utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "class" : "form-control text-center",
                "placeholder" : "..."
            }),label="Mot de Passe")
    
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
    
class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class' : "form-control",
        "placeholer" : "provide the mail used for customer account ...",        
    }))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if Customer.objects.filter(user__email=email).exists():
            pass 
        else :
            raise forms.ValidationError('User with this email does not exists')
            
        return email



class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        'autocomplete' : "new password",
        "placeholder" : "Enter the new password",
    
    }),label="Entrer votre nouveau mot de Passe ")
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
    "class": "form-control",
    'autocomplete' : "confirm password",
    "placeholder" : "Confirm the new password",

}),label="Confirmer votre nouveau mot de Passe ")
    
def clean_confirm_password(self):
    new_password = self.clean_data.get("new_password")
    confirmed_password = self.clean_data.get("confirm_password")
    if new_password != confirmed_password :
        raise forms.ValidationError("The passwords are not match !! ")    
    return confirmed_password
    
   
    
   
