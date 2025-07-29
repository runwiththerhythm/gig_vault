from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def my_gigs(request):
    return HttpResponse("Hello, gigs!")
