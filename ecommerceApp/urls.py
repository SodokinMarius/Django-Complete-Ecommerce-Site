from django.urls import path

from .views import (
    AboutView,
    HomeView,
    ContactView,
    ProductsView,
    ProductDetailView, 
    AddToCartView,  
    CartContentView,
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

]
