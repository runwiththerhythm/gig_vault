from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Gig

# Create your views here.

# Main dashboard My Gig Vault view
@login_required
def gigs_dashboard(request):
    attended_gigs = Gig.objects.filter(user=request.user).order_by('-date')[:50]
    upcoming_gigs = Gig.objects.filter(user=request.user, status='upcoming').order_by('date')[:50]


    return render(request, "gigs/dashboard.html", {
        "attended_gigs": attended_gigs,
        "upcoming_gigs": upcoming_gigs
    })