from django.shortcuts import render

def site_home(request):
    return render(request, 'home.html')