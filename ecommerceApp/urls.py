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
    CustomerLoginView,
    CustomerLogoutView,
    CustomerProfileView,
    CustomerOrderDetailView,
    AdminLoginView,
    AdminHomeView,
    AdminAllOrderView,
    AdminOrderDetailView, 
    AdminOrderStatusChangeView,
    ReSearchView,
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
    path("customer-login/",CustomerLoginView.as_view(),name='customer-login'),
    path("customer-logout/",CustomerLogoutView.as_view(),name='customer-logout'),
    path("customer-profile/",CustomerProfileView.as_view(),name='customer-profile'),
    path("customer-order-detail/<int:pk>/",CustomerOrderDetailView.as_view(),name='customer-order-detail'),
    path("admin-login/",AdminLoginView.as_view(),name='admin-login'),
    path("admin-home/",AdminHomeView.as_view(),name='admin-home'),
    path("admin-all-order/",AdminAllOrderView.as_view(),name='admin-all-order'),
    path("admin-order-detail/<int:pk>/",AdminOrderDetailView.as_view(),name='admin-order-detail'),
    path("admin-order/<int:pk>/change",AdminOrderStatusChangeView.as_view(),name='admin-order-change'),
    path("research/",ReSearchView.as_view(),name='search-product'),


]
