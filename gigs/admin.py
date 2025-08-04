from django.contrib import admin
from .models import Band, Venue, Gig

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')  # assuming you added location field
    search_fields = ('name', 'location')
    ordering = ('name',)

@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('band', 'venue', 'date')
    search_fields = ('band__name', 'venue__name')
    list_filter = ('date',)
    ordering = ('-date',)