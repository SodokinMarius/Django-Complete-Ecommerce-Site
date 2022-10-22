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
