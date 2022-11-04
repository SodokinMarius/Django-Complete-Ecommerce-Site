
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View, CreateView,FormView,DetailView,ListView #We can use FormModel instead of CreateView

from .models import *
from django.contrib.auth.models import User

from .forms import CheckoutForm,RegistrationForm,CustomerLoginForm,ProductForm,PasswordForgotForm,PasswordResetForm

from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q 

from django.core.paginator import Paginator

from .utils import password_reset_token

from django.core.mail import send_mail  

from django.conf import settings     



#Let's assign the cart to a customer
class EcommerceMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)        
           
#Home view
class HomeView(TemplateView,EcommerceMixin):
    template_name="home.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        all_product_list = Product.objects.all().order_by('-title')
        paginator = Paginator( all_product_list,3)
        
        page_number = self.request.GET.get('page')

        product_list = paginator.get_page(page_number)
        
        context['products']= product_list
        return  context
   

class AboutView(TemplateView,EcommerceMixin):
    template_name = "about.html"


class ContactView(TemplateView,EcommerceMixin):
    template_name = "contact.html"


class ProductsView(TemplateView,EcommerceMixin):
    template_name="produits.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)           
        
        all_category_list = Category.objects.all().order_by('title')
        paginator = Paginator( all_category_list ,3)
        
        page_number = self.request.GET.get('page')

        category_list = paginator.get_page(page_number)
        
        context['categories']= category_list
        
        return  context
    

class ProductDetailView(TemplateView,EcommerceMixin):
    template_name="product-detail.html"
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        retrieved_slug=kwargs['slug']
        produit=Product.objects.get(slug=retrieved_slug)
        produit.view_count+=1
        produit.save()
        context['produit_detail']=produit
        return  context

  
class  AddToCartView(TemplateView,EcommerceMixin):
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
    
    
class CartContentView(TemplateView,EcommerceMixin):
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
    
class CartManageView(View,EcommerceMixin):
    def get(self, request,*args,**kargs):
        cartproduct_id = self.kwargs['cartproduct_id']
        action = request.GET.get("action")
        cartproduct_obj = CartProduct.objects.get(id=cartproduct_id)
        cart_for_product =  cartproduct_obj.cart
              
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
    

class EmptyCartView(View,EcommerceMixin):
    def get(self, request,*args,**kwargs):
        
        cart_id = self.request.session.get('cart_id')
        if cart_id :
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()            
        
        return redirect("ecommerceApp:empty-cart")
    
    
class CheckoutView(CreateView,EcommerceMixin):
    template_name =  "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy('ecommerceApp:home')  # success_url --> keyWord
    
    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists(): #si le user est authentifié et est un client
            pass
        else :
            return redirect("/customer-login/?next=/checkout/")
            
        return super().dispatch(request, *args, **kwargs)
    
    
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
           return redirect("ecommerceApp:home")                
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
        
        if user_in_connexion is not None and Customer.objects.filter(user=user_in_connexion).exists() :
            login(
                self.request,
                user_in_connexion
            )
        else :
            return render(self.request, self.template_name, context = {'form': self.form_class, 'errors' : "Identififiants incorrects" })
        return super().form_valid(form)
    
    #Manage the redirect URL after logging in to checkout
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url



class CustomerLogoutView(View):
    def get(self,*args, **kwargs) :
        logout(self.request)
        
        return redirect('ecommerceApp:home')
    

class CustomerProfileView(TemplateView,EcommerceMixin):
    template_name =  "customer_profile.html"
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/customer-login/?next=/customer-profile/")
        return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        orders = Order.objects.filter(cart__customer=customer)
        print("Nombre de commande : "+ str(orders.count()))
        context['customer'] = customer
        context['orders'] = orders
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "customer-order-detail.html" 
    model = Order
    context_object_name = 'order'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            
            #verifions si la commande demandée est effectueé par le client en cours
            current_customer = Order.cart.customer
            if self.request.user.customer != current_customer :
                return redirect("ecommerceApp:customer-profile")
        else:
            return redirect("/customer-login/?next=/customer-profile/")
        return super().dispatch(request, *args, **kwargs)


#=============================== ADMIN VIEWS ===================================
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass 
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)
    
    
class AdminLoginView(FormView,AdminRequiredMixin):
    template_name = "adminPages/admin_login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecommerceApp:admin-home')
    
    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user_in_connexion = authenticate(username = username, password = password)
        
        if user_in_connexion is not None and Admin.objects.filter(user=user_in_connexion).exists() :
            login(
                self.request,
                user_in_connexion
            )
        else :
            return render(self.request, self.template_name, context = {'form': self.form_class, 'errors' : "Identififiants incorrects" })
        return super().form_valid(form)
    
class AdminHomeView(TemplateView,AdminRequiredMixin) :
    template_name = "adminPages/admin_home.html"
       
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        placed_orders = Order.objects.filter(order_status="Order Received")
        context['placed_orders'] = placed_orders 
        return context
        
    
    
class AdminAllOrderView(ListView,AdminRequiredMixin):
    template_name = "adminPages/admin_all_orders.html"
    queryset = Order.objects.all().order_by('id')
    context_object_name = "orders"
    
    
class AdminOrderDetailView(DetailView,AdminRequiredMixin):
    template_name = "adminPages/admin_order_detail.html"
    model = Order
    context_object_name = "order"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_status'] = STATUS_CHOICES
        return context
    

class AdminOrderStatusChangeView(View,AdminRequiredMixin):
    def post(self,request, *args,**kwargs):
        order_id = self.kwargs["pk"]
        
        order = Order.objects.get (id=order_id)
        order_status = request.POST.get("status")
        order.order_status = order_status
        order.save()
        return redirect(reverse_lazy("ecommerceApp:admin-order-change",kwargs = {"pk": order_id}))
    

class ReSearchView(TemplateView,AdminRequiredMixin):
    template_name = 'research.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)  
        keyword = self.request.GET.get('product_keyword')  
        context["keyword"] = keyword 
        print(f'{keyword},-----------------------------------------')
        context["found_products"] = Product.objects.filter(Q(title__startswith=keyword) | Q(description__contains=keyword) | Q(return_policy__contains=keyword))
        return context  
    
    
class AdminProductsView(AdminRequiredMixin,ListView):
    template_name = "adminPages/admin_products.html"
    queryset = Product.objects.all().order_by('-id')
    context_object_name = "products"
        
class AdminAddProductView(AdminRequiredMixin,CreateView):
    template_name =  "adminPages/admin_add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy('ecommerceApp:admin-products')  
    
    def form_valid(self, form):
        product = form.save()
        images = self.request.FILES.getlist('more_images')
        
        print(f'{product.title},-------------------------------1----------')

        for image in images :
            img = ProductImage.objects.create(product=product,image=image)
            print(f'{img.product.title},-----------------222p--------------1----------')
        return super().form_valid(form) 
    

class PasswordForgotView(FormView):
    template_name = "password_forgot.html"
    form_class = PasswordForgotForm 
    success_url = "/password-forgot/?msg=sent"
    
    def form_valid(self, form):
        _email = form.cleaned_data.get('email') 
        print(_email,"email *****************************")
        customer = Customer.objects.get(user__email=_email)
        user = customer.user
        url = self.request.META.get('HTTP_HOST') 
        text_content = "Please, Click the link below to reset your password !"
        html_content = url + '/password-reset/' + _email +'/' + password_reset_token.make_token(user) + '/' 
        
        send_mail(
            "Password Reset link | DIGIT Ecommerce",
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [_email],
            fail_silently=False,
        )       
              
        return super().form_valid(form)
    
    
class EmailSentView(View):
   def get(self,request,*args,**kwargs):
       return redirect(reverse_lazy('ecommerceApp:password-forgot'))

class PasswordResetView(FormView):
    template_name = 'password_reset.html'
    form_class = PasswordResetForm 
    success_url = reverse_lazy('ecommerceApp:customer-login')
    
    
    def dispatch(self, request, *args, **kwargs) :
        email = self.kwargs.get("email")
        print("Token :",self.request.GET.get("email"),"----------------")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user,token): 
            pass 
        else :
            return redirect(reverse_lazy('ecommerceApp:password-forgot') + "?msg=error")    #make user retake the password reset form filling      
           
        return super().dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form) :
        password = form.cleaned_data.get('confirm_password')
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)            
        user.save()
        return super().form_valid(form)
    
    
    
    
    