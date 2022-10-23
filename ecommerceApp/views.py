from django.shortcuts import render
from django.views.generic import TemplateView

from .models import *


#Home view
class HomeView(TemplateView):
    template_name="home.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['products']=Product.objects.all().order_by('-title')
        return  context
   

class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class ProductsView(TemplateView):
    template_name="produits.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['categories']=Category.objects.all().order_by('title')
        return  context

class ProductDetailView(TemplateView):
    template_name="product-detail.html"
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        retrieved_slug=kwargs['slug']
        produit=Product.objects.get(slug=retrieved_slug)
        produit.view_count+=1
        produit.save()
        context['produit_detail']=produit
        return  context

  
class  AddToCartView(TemplateView):
    template_name="add_to_cart.html"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id=self.kwargs['id']
        product=Product.objects.get(id=product_id) # let's retrieve the product
        
        print(f'{product_id} ***********id***********************')

        #retrive cart_id
        cart_id=self.request.session.get("cart_id",None)    # Retrive the cart id
        
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id) # Retrieve the cart obj
            
            #verifying that the product exists in the cart
       
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product) 
            if this_product_in_cart.exists():
                cartproduct =this_product_in_cart.first()
                cartproduct.quantity += 1
                cartproduct.subtotal += product.selling_price
                cartproduct.save()
                
                cart_obj.total += product.selling_price
                cart_obj.save()
            else :
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product,
                    rate=product.selling_price,
                    quantity=1,
                    subtotal = product.selling_price
                    ) 
                
                #cartproduct.save()
                cart_obj.total += product.selling_price
                print(f'{cart_obj.total} ***********prix***********************')
                cart_obj.save()
                
        #if Cart doesn't exists
        else :
            cart_obj = Cart.objects.create(total=0)
            self.request.session["cart_id"]=cart_obj.id  #Obligatoire de modifier la session
            cartproduct = CartProduct.objects.create(
                    cart=cart_obj,
                    product=product,
                    rate=product.selling_price,
                    quantity=1,
                    subtotal = product.selling_price
                    ) 
                
            #cartproduct.save()
            cart_obj.total += product.selling_price
            cart_obj.save()

            context['cartproduct']=cartproduct
            context['message']="Added successfully !"
            
        return context
    
    
class CartContentView(TemplateView):
    template_name="cart_content.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cart_id=self.request.session.get("cart_id",None)
        print(f'{cart_id} **********ID CART***********************')

        
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else :
            cart = None 
        context['cart']=cart  
        print(f'{cart} **********CART***********************')
          
        return context
        
