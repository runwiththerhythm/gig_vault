from django.shortcuts import render
from django.views.generic import TemplateView


# About page view
class AboutView(TemplateView):
    template_name = "about.html"


# Home page view
def site_home(request):
    return render(request, 'home.html')
