from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField

# Create your models here.

class Gig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True, related_name="headline_gigs")
    tour_title = models.CharField(max_length=255, blank=True, help_text="Tour/Festival name (optional)")
    other_artists = models.ManyToManyField(Band, blank=True, )
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField()
    is_festival = models.BooleanField(default=False)
    notes = SummernoteTextField(blank=True)

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
          """
        Returns a human-readable title for the gig, combining:
        - Band name (or fallback text)
        - Optional tour title
        - Venue name
        - Date
        Formatted with separators for clarity in lists or menus.
        """
    band_name = self.band.name if self.band else "Unknown Band"
    if self.tour_title:
        name = f"{band_name} — {self.tour_title} @ {self.venue.name}"
    else:
        name = f"{band_name} @ {self.venue.name}"
    return f"{name} — {self.date.strftime('%Y-%m-%d')}"