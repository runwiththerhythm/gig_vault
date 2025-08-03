from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Gig
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

# Main dashboard My Gig Vault view - Function based view for dashboard
@login_required
def gigs_dashboard(request):
    attended_gigs = Gig.objects.filter(user=request.user).order_by('-date')[:50]
    upcoming_gigs = Gig.objects.filter(user=request.user, status='upcoming').order_by('date')[:50]


    return render(request, "gigs/dashboard.html", {
        "attended_gigs": attended_gigs,
        "upcoming_gigs": upcoming_gigs
    })

# Class based views for CRUD implementations

# Gig list view
class GigListView(LoginRequiredMixin, ListView):
    model = Gig
    template_name = 'gigs/gig_list.html'
    context_object_name = 'gigs'

    def get_queryset(self):
        return Gig.objects.filter(user=self.request.user).order_by('-date')

# Create gig view
class GigCreateView(LoginRequiredMixin, CreateView):
    model = Gig
    fields = ['band_name', 'date', 'location', 'status', 'notes']
    template_name = 'gigs/gig_form.html'
    success_url = reverse_lazy('gig_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Gig detail view
class GigDetailView(LoginRequiredMixin, DetailView):
    model = Gig
    template_name = 'gigs/gig_detail.html'
    context_object_name = 'gig'

    def get_queryset(self):
        return Gig.objects.filter(user=self.request.user)