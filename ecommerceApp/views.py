from django.shortcuts import render
from django.views.generic import TemplateView


#Home view
class HomeView(TemplateView):
    template_name="home.html"
   


class AboutView(TemplateView):
    template_name = "about.html"