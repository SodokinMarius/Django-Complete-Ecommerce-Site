from queue import Empty
from django.urls import path

from .views import (
    AboutView,
    HomeView,
    ContactView,
    ProductsView,
    ProductDetailView, 
    AddToCartView,  
    CartContentView,
    CartManageView,
    EmptyCartView,
    CheckoutView,
    RegistrationView,
)

app_name="ecommerceApp"
urlpatterns = [
    path("",HomeView.as_view(),name="home"),
    path("about/",AboutView.as_view(),name="about"),
    path("contact/",ContactView.as_view(),name="contact"),
    path("products/",ProductsView.as_view(),name="products"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="product-detail"),
    path("add-to-cart/<int:id>/",AddToCartView.as_view(),name="add-to-cart"),
    path("cart-content/",CartContentView.as_view(),name="cart-content"),
    path("cart-manage/<int:cartproduct_id>/",CartManageView.as_view(),name="cart-manage"),
    path("empty-cart/",EmptyCartView.as_view(),name='empty-cart'),
    path("checkout/",CheckoutView.as_view(),name='checkout'),
    path("registration/",RegistrationView.as_view(),name='customer-registration'),

]
