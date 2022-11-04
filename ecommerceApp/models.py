
from django.db import models

from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=60)
    telephone = models.CharField(max_length=30)
    profile_photo = models.ImageField(upload_to="Admins")
    
    def __str__(self) :
        return self.full_name
    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300,verbose_name='Nom Complet')
    telephone = models.CharField(max_length=30,verbose_name='Numéro de téléphone')
    adresse = models.CharField(max_length=300,null=True,blank=True,verbose_name='Adresse de residence')
    joined_on = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.full_name
    
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return  self.title

class Product(models.Model):
    title = models.CharField(max_length=200,verbose_name='Titre')
    slug = models.SlugField(unique=True,verbose_name='Nom Unique')
    category =  models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='Categorie')
    image = models.ImageField(upload_to='products',verbose_name='Image')
    marked_price = models.PositiveBigIntegerField(verbose_name="Prix D'Achat")
    selling_price = models.PositiveBigIntegerField(verbose_name='Prix de Vente')
    description = models.TextField(verbose_name='Description')
    warranty = models.CharField(max_length=300, null=True,blank=True,verbose_name='Garantie')
    return_policy = models.CharField(max_length=300, null=True,blank=True,verbose_name='Politique de retour')
    view_count = models.PositiveIntegerField(default=0,verbose_name='Titre')
    
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to="products/images")
    
    def __str__(self) :
        return self.product.title
        
    
class Cart(models.Model):    
    customer= models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Cart : "+str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate =  models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveBigIntegerField()
          
    def __str__(self):
        return "Cart : "+str(self.id)+" Product : "+str(self.product.id)+" CardProduct : "+str(self.id)
    

STATUS_CHOICES=(
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Cancelled", "Order Cancelled"),
    ("Order Completed", "Order Completed"),    
)

class Order(models.Model):    
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by =  models.CharField(max_length=200)
    shipping_adress = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(null=True,blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total =  models.PositiveIntegerField()
    order_status = models.CharField(max_length=20,choices=STATUS_CHOICES)
    created_at =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return ' Order : '+ str(Order.id)
    
    



