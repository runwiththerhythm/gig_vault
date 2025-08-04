from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField

# Create your models here.

# Band model
class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Venue model
class Venue(models.Model):
    name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)  # optional

    def __str__(self):
        return f"{self.name} ({self.location})" if self.location else self.name

# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
        
# Gig Images model
class GigImage(models.Model):
    gig = models.ForeignKey("Gig", on_delete=models.CASCADE, related_name="images")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField("Gig Image", default="placeholder", null=False, blank=False)
    is_cover = models.BooleanField(default=False, help_text="Set as cover image for the gig")

    class Meta:
        ordering = ["-is_cover", "id"]

    def __str__(self):
        return f"Image for {self.gig.get_display_name()}"
    
    def save(self, *args, **kwargs):
        if self.is_cover and (not self.pk or not GigImage.objects.get(pk=self.pk).is_cover):
            GigImage.objects.filter(gig=self.gig, is_cover=True).exclude(pk=self.pk).update(is_cover=False)
        super().save(*args, **kwargs)



# Main Gig model
class Gig(models.Model):

    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("attended", "Attended"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True, related_name="headline_gigs")
    tour_title = models.CharField(max_length=255, blank=True, help_text="Tour/Festival name (optional)")
    other_artists = models.ManyToManyField(Band, blank=True, )
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    is_festival = models.BooleanField(default=False)
    notes = SummernoteTextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="attended")

    class Meta:
        ordering = ["date"]

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

