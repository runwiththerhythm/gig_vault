from django.urls import path
from .views import (
    gigs_dashboard,
    GigListView,
    GigCreateView,
    GigDetailView,
    GigUpdateView,
    GigDeleteView,
)

urlpatterns = [
    path('', gigs_dashboard, name='dashboard'),            # /dashboard/
    path('gigs/', GigListView.as_view(), name='gig_list'),  # /dashboard/gigs/
    path('gigs/new/', GigCreateView.as_view(), name='gig_create'),  # /dashboard/gigs/new/
    path('gigs/<int:pk>/', GigDetailView.as_view(), name='gig_detail'),  # /dashboard/gigs/<pk>/
    path('gigs/<int:pk>/edit/', GigUpdateView.as_view(), name='gig_edit'),  # /dashboard/gigs/<pk>/edit/
    path('gigs/<int:pk>/delete/', GigDeleteView.as_view(), name='gig_delete'),  # /dashboard/gigs/<pk>/delete/
]
