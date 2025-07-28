from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def my_gigs(request):
    return HttpResponse("Hello, gigs!")
