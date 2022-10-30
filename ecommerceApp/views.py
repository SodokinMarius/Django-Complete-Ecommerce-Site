from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View, CreateView,FormView #We can use FormModel instead of CreateView

from .models import *
from django.contrib.auth.models import User

from .forms import CheckoutForm,RegistrationForm,CustomerLoginForm

from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout


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
    
class CartManageView(View):
    def get(self, request,*args,**kargs):
        cartproduct_id = self.kwargs['cartproduct_id']
        action = request.GET.get("action")
        cartproduct_obj = CartProduct.objects.get(id=cartproduct_id)
        cart_for_product =  cartproduct_obj.cart
        
        '''cart_id_in_session = self.request.session.get("cart_id",None)
        if cart_id_in_session:
            cart_obj_in_session = Cart.objects.get(id=cart_id_in_session)'''
        
        if action == 'increase':
            cartproduct_obj.quantity += 1
            cartproduct_obj.subtotal +=  cartproduct_obj.rate
            cartproduct_obj.save()
            
            cart_for_product.total += cartproduct_obj.rate
            cart_for_product.save()
                       
        elif action == 'decrease':
            cartproduct_obj.quantity -= 1
            cartproduct_obj.subtotal -=  cartproduct_obj.rate
            cartproduct_obj.save()
            
            cart_for_product.total -= cartproduct_obj.rate
            cart_for_product.save()
            
            # Si la quantité est nulle après diminution, on le supprime
            if cartproduct_obj.quantity == 0 :
                cart_for_product.delete()
             
        elif action == 'delete' :
            cart_for_product.total -= cartproduct_obj.subtotal
            cart_for_product.save()
            cartproduct_obj.delete()
            
        else :
            pass
        return redirect('ecommerceApp:cart-content')
    

class EmptyCartView(View):
    def get(self, request,*args,**kwargs):
        
        cart_id = self.request.session.get('cart_id')
        if cart_id :
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()            
        
        return redirect("ecommerceApp:empty-cart")
    
    
class CheckoutView(CreateView):
    template_name =  "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy('ecommerceApp:home')  # success_url --> keyWord
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart 
        return context

    def form_valid(self, form):
        cart_id =  self.request.session.get("cart_id")
        
        if cart_id :
            cart = Cart.objects.get(id=cart_id)
            form.instance.cart  = cart
            form.instance.subtotal = cart.total
            
            form.instance.discount = 0
            form.instance.total = cart.total
            
            form.instance.order_status = "Order Received"
            del self.request.session["cart_id"]  #Supprimer le panier de la session
        else :
            redirect("ecommerceApp:home")                
        return super().form_valid(form)


class RegistrationView(CreateView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('ecommerceApp:home')
    
    def form_valid(self, form) :        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        
        user = User.objects.create_user(username=username,password=password,email=email)
       
        form.instance.user = user
        login(self.request,user)
        return super().form_valid(form)
    

class CustomerLoginView(FormView):
    template_name = "customerLogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecommerceApp:home')
    
    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user_in_connexion = authenticate(username = username, password = password)
        
        if user_in_connexion is not None and user_in_connexion.customer :
            self.request.session['user'] = user_in_connexion
            login(
                self.request,
                user_in_connexion
            )
        else :
            return render(self.request, self.template_name, context = {'form': self.form_class, 'errors' : "Identififiants incorrects" })
        return super().form_valid(form)


class CustomerLogoutView(View):
    def get(self,*args, **kwargs) :
        logout(self.request)
        
        return redirect('ecommerceApp:home')
    
        
           
       
        
