import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.urls import reverse_lazy, reverse
from dal import autocomplete
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q



from .models import Band, Venue, Gig, GigImage, GigVideo
from .forms import GigForm, GigImageFormSet, GigVideoFormSet


# Create your views here.

# Main dashboard My Gig Vault view - Function based view for dashboard
@login_required
def gigs_dashboard(request):
    attended_gigs = (
        Gig.objects.filter(
            user=request.user,
            status='attended'
        ).order_by('-date')[:50]
    )
    upcoming_gigs = (
        Gig.objects.filter(
            user=request.user,
            status='upcoming'
        ).order_by('date')[:50]
    )

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_token'] = os.environ.get('MAPBOX_TOKEN')
        # Create:
        if isinstance(self, GigCreateView):
            context['formset'] = GigImageFormSet(instance=Gig())
        # Update:
        else:
            if self.request.method == "POST":
                context['formset'] = GigImageFormSet(
                    self.request.POST, self.request.FILES,
                    instance=self.object)
            else:
                context['formset'] = GigImageFormSet(
                    instance=self.object)
        return context

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
            form.instance.venue = None

        # Save the Gig
        self.object = form.save()


# Add all files from the multi-upload field
        for f in self.request.FILES.getlist("images"):
            GigImage.objects.create(
                gig=self.object, user=self.request.user, image=f)

        if not self.object.images.filter(is_cover=True).exists():
            first = self.object.images.first()
            if first:
                first.is_cover = True
                first.save(update_fields=["is_cover"])

        return redirect(self.get_success_url())

        def get_success_url(self):
            return reverse_lazy("my_gigs")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_token'] = os.environ.get('MAPBOX_TOKEN')

        # Provide the inline formset for existing images
        if self.request.method == "POST":
            context['formset'] = GigImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = GigImageFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Venue handling
        venue_name = self.request.POST.get("venue_name", "").strip()
        venue_city = self.request.POST.get("venue_city", "").strip()
        venue_country = self.request.POST.get("venue_country", "").strip()

        if venue_name:
            venue, _ = Venue.objects.get_or_create(
                name=venue_name,
                defaults={"city": venue_city, "country": venue_country},
            )
            form.instance.venue = venue
        else:
            form.instance.venue = None

        self.object = form.save()

        # Add new files from multi-upload
        for f in self.request.FILES.getlist("images"):
            GigImage.objects.create(
                gig=self.object, user=self.request.user, image=f)

        # Process inline formset: edit/delete + cover
        formset = GigImageFormSet(
            self.request.POST, self.request.FILES, instance=self.object)

        if formset.is_valid():
            instances = formset.save(commit=False)

            for to_del in formset.deleted_objects:
                to_del.delete()

            for inst in instances:
                inst.gig = self.object
                inst.user = self.request.user
                inst.save()

            formset.save_m2m()
        else:
            return self.form_invalid(form)

        # Ensure exactly one cover
        if not self.object.images.filter(is_cover=True).exists():
            first = self.object.images.first()
            if first:
                first.is_cover = True
                first.save(update_fields=["is_cover"])

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("my_gigs")


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
        """
        For AJAX: return JSON {id, name}.
        De-duplicate: If a Band with case-insensitive same name exists,
        return that instead of creating a new one.
        """
        name = form.cleaned_data.get("name", "").strip()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            existing = Band.objects.filter(name__iexact=name).first()
            if existing:
                self.object = existing
            else:
                self.object = form.save()
            return JsonResponse(
                {"id": self.object.id, "name": self.object.name})
        # Non-AJAX fallback
        existing = Band.objects.filter(name__iexact=name).first()
        if existing:
            self.object = existing
            return super().form_valid(form)  # redirects as usual
        self.object = form.save()
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
        return next_url or reverse_lazy('gig_create')


@login_required
def manage_gig_videos(request, pk):
    gig = get_object_or_404(Gig, pk=pk, user=request.user)

    if request.method == "POST":
        formset = GigVideoFormSet(request.POST, instance=gig)
        if formset.is_valid():
            # attach user to new forms
            instances = formset.save(commit=False)
            for obj in instances:
                if not obj.added_by_id:
                    obj.added_by = request.user
                obj.save()
            # handle deletions
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "Videos updated.")
            return redirect(reverse("gig_detail", args=[gig.pk]))
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        formset = GigVideoFormSet(instance=gig)

    return render(
        request,
        "gigs/gig_videos.html",
        {"gig": gig, "formset": formset}
    )

# --- AJAX lookup for duplicates (typeahead / hints) ---


@login_required
@require_GET
def band_lookup_ajax(request):
    """
    GET /bands/lookup/?q=term
    Returns JSON with an exact match (case-insensitive) if present,
    and up to 5 similar names.
    """
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"exact": None, "similar": []})

    exact = Band.objects.filter(name__iexact=q).values("id", "name").first()
    similar = list(
        Band.objects.filter(name__icontains=q)
        .exclude(name__iexact=q)
        .order_by("name")
        .values_list("name", flat=True)[:5]
    )
    return JsonResponse({"exact": exact, "similar": similar})


# --- AJAX delete for Undo (guard if referenced by any Gig) ---
@login_required
@require_POST
def band_delete_ajax(request, pk: int):
    """
    Deletes a Band only if it is not referenced by any gigs
    (as headliner or support).
    200: {"ok": True} on success
    409: {"ok": False, "reason": "in_use"} if it is referenced
    """
    band = get_object_or_404(Band, pk=pk)
    in_use = Gig.objects.filter(Q(band=band) | Q(other_artists=band)).exists()
    if in_use:
        return JsonResponse({"ok": False, "reason": "in_use"}, status=409)

    band.delete()
    return JsonResponse({"ok": True})
