from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def gigs_dashboard(request):
    return render(request, "gigs/dashboard.html")