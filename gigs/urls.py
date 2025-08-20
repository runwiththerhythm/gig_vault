from django.urls import path
from .views import (
    gigs_dashboard,
    MyGigsView, GigCreateView, GigDetailView, GigUpdateView, GigDeleteView,
    BandAutocomplete, BandCreateView,
    VenueAutocomplete, VenueCreateView,
    manage_gig_videos,
    band_lookup_ajax, band_delete_ajax,
)

urlpatterns = [
    path('', gigs_dashboard, name='dashboard'),
    path('gigs/', MyGigsView.as_view(), name='my_gigs'),
    path('gigs/new/', GigCreateView.as_view(), name='gig_create'),
    path('gigs/<int:pk>/', GigDetailView.as_view(), name='gig_detail'),
    path('gigs/<int:pk>/edit/', GigUpdateView.as_view(), name='gig_edit'),
    path('gigs/<int:pk>/delete/', GigDeleteView.as_view(), name='gig_delete'),

    path('band-autocomplete/', BandAutocomplete.as_view(),
         name='band-autocomplete'),
    path('bands/add/', BandCreateView.as_view(), name='band_create'),

    path('venue-autocomplete/', VenueAutocomplete.as_view(),
         name='venue-autocomplete'),
    path('venues/add/', VenueCreateView.as_view(), name='venue_create'),

    path("gigs/<int:pk>/videos/", manage_gig_videos, name="gig_videos"),

    path("bands/lookup/", band_lookup_ajax, name="band_lookup_ajax"),
    path("bands/<int:pk>/delete/", band_delete_ajax, name="band_delete_ajax"),]
