from django.urls import path
from .views import gigs_dashboard

urlpatterns = [
    path('', gigs_dashboard, name='dashboard'),]