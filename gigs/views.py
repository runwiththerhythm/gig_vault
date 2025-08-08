from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Gig
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import GigForm
from dal import autocomplete
from .models import Band, Venue
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os


# Create your views here.

# Main dashboard My Gig Vault view - Function based view for dashboard
@login_required
def gigs_dashboard(request):
    attended_gigs = Gig.objects.filter(user=request.user, status='attended').order_by('-date')[:50]
    upcoming_gigs = Gig.objects.filter(user=request.user, status='upcoming').order_by('date')[:50]

    return render(request, "gigs/dashboard.html", {
        "attended_gigs": attended_gigs,
        "upcoming_gigs": upcoming_gigs
    })

# Class based views for CRUD implementations

# My gigs view
class MyGigsView(LoginRequiredMixin, ListView):
    model = Gig
    template_name = 'gigs/my_gigs.html'
    context_object_name = 'gigs'

    def get_queryset(self):
        return Gig.objects.filter(user=self.request.user).order_by('-date')

# Create gig view
class GigCreateView(LoginRequiredMixin, CreateView):
    model = Gig
    form_class = GigForm
    template_name = 'gigs/gig_form.html'
    success_url = reverse_lazy('my_gigs')

    def get_initial(self):
        initial = super().get_initial()
        band_id = self.request.GET.get('band_id')
        if band_id:
            initial['band'] = Band.objects.get(id=band_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user


        venue_name = self.request.POST.get("venue_name", "").strip()
        venue_city = self.request.POST.get("venue_city", "").strip()
        venue_country = self.request.POST.get("venue_country", "").strip()
        
        print("Venue fields from POST:", venue_name, venue_city, venue_country)


        if venue_name:

            venue, _ = Venue.objects.get_or_create(
                name=venue_name,
                defaults={
                    "city": venue_city,
                    "country": venue_country,
                }
            )
            form.instance.venue = venue

        else:
            form.instance.venue = None  # Optional fallback

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_gigs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_token'] = os.environ.get('MAPBOX_TOKEN')
        return context


# Gig detail view
class GigDetailView(LoginRequiredMixin, DetailView):
    model = Gig
    template_name = 'gigs/gig_detail.html'
    context_object_name = 'gig'

    def get_queryset(self):
        return Gig.objects.filter(user=self.request.user)

# Gig update view
class GigUpdateView(LoginRequiredMixin, UpdateView):
    model = Gig
    form_class = GigForm
    template_name = 'gigs/gig_form.html'
    success_url = reverse_lazy('my_gigs')

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Get venue data from POST
        venue_name = self.request.POST.get("venue_name", "").strip()
        venue_city = self.request.POST.get("venue_city", "").strip()
        venue_country = self.request.POST.get("venue_country", "").strip()

        print("Venue fields from POST:", venue_name, venue_city, venue_country)


        if venue_name:
            venue, _ = Venue.objects.get_or_create(
                name=venue_name,
                defaults={
                    "city": venue_city,
                    "country": venue_country,
                }
            )
            form.instance.venue = venue
        else:
            form.instance.venue = None  # Optional fallback

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_token'] = os.environ.get('MAPBOX_TOKEN')
        return context
        
# Gig delete view
class GigDeleteView(LoginRequiredMixin, DeleteView):
    model = Gig
    template_name = 'gigs/gig_confirm_delete.html'
    success_url = reverse_lazy('my_gigs')

    def get_queryset(self):
        return Gig.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_token'] = settings.MAPBOX_TOKEN
        return context


# Band autocomplete
class BandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Band.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

# Add new band view
class BandCreateView(LoginRequiredMixin, CreateView):
    model = Band
    fields = ['name']
    template_name = 'gigs/band_form.html'

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'id': self.object.id,
                'name': self.object.name,
            })
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('gig_create')

# Venue autocomplete
class VenueAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Venue.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

# Add new venue view
class VenueCreateView(LoginRequiredMixin, CreateView):
    model = Venue
    fields = ['name']
    template_name = 'gigs/venue_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url or reverse('gig_create')