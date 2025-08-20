from django.contrib import admin
from .models import Band, Venue, Gig, GigVideo


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    search_fields = ('name', 'city', 'country')
    list_filter = ('city', 'country',)
    ordering = ('name',)


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('date', 'band', 'venue', 'is_festival', 'status',)
    list_filter = ('status', 'is_festival', 'date',)
    search_fields = ('band__name', 'venue__name', 'tour_title',)
    ordering = ('-date',)
    date_hierarchy = 'date'
    list_select_related = ('band', 'venue')
    autocomplete_fields = ('band', 'venue', 'other_artists')

    def get_queryset(self, request):
        # speed up admin list by joining FK tables
        qs = super().get_queryset(request)
        return qs.select_related('band', 'venue')


@admin.register(GigVideo)
class GigVideoAdmin(admin.ModelAdmin):
    list_display = ("gig", "title", "video_id", "is_featured", "added_at")
    list_filter = ("is_featured", "added_at")
    search_fields = ("title", "url", "gig__band__name", "gig__venue__name")
