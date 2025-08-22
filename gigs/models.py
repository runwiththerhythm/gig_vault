from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_summernote.fields import SummernoteTextField
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
import re
from urllib.parse import urlparse, parse_qs

# Create your models here.


# Band model
class Band(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Venue model
class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self):
        location = ", ".join(filter(None, [self.city, self.country]))
        return f"{self.name} ({location})" if location else self.name


# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


# Gig Images model
class GigImage(models.Model):
    gig = models.ForeignKey(
        "Gig",
        on_delete=models.CASCADE,
        related_name="images"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    image = CloudinaryField(
        "Gig Image",
        default="placeholder",
        null=False,
        blank=False
    )
    is_cover = models.BooleanField(
        default=False,
        help_text="Set as cover image for the gig"
    )

    class Meta:
        ordering = ["-is_cover", "id"]

    def __str__(self):
        return f"Image for {self.gig.get_display_name()}"

    def save(self, *args, **kwargs):
        if self.is_cover and (
                not self.pk or not GigImage.objects.get(pk=self.pk).is_cover):
            GigImage.objects.filter(
                gig=self.gig, is_cover=True).exclude(
                    pk=self.pk).update(is_cover=False)
        super().save(*args, **kwargs)


# Main Gig model
class Gig(models.Model):

    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("attended", "Attended"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gigs"
    )
    band = models.ForeignKey(
        Band,
        on_delete=models.SET_NULL,
        null=True,
        related_name="headline_gigs"
    )
    tour_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Tour/Festival name (optional)"
    )
    other_artists = models.ManyToManyField(
        Band,
        blank=True
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date = models.DateField()
    is_festival = models.BooleanField(default=False)
    notes = SummernoteTextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="attended"
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self):
        band_name = self.band.name if self.band else "Unknown Band"
        venue_display = self.venue.name if self.venue else "Unknown Venue"

        if self.tour_title:
            name = f"{band_name} — {self.tour_title} @ {venue_display}"
        else:
            name = f"{band_name} @ {venue_display}"

        return f"{name} — {self.date.strftime('%Y-%m-%d')}"

    def get_cover_image(self):
        """Return the cover image, or fallback to first, or None."""
        cover = self.images.filter(is_cover=True).first()
        if cover:
            return cover.image.url
        first = self.images.first()
        if first:
            return first.image.url
        return None

    def youtube_query(self) -> str:
        """
        Build a sensible YouTube search query:
        - If festival: use the band field (festival name) + year
        - Else if tour_title given: <Band> <TourTitle> <Year>
        - Else fallback: <Band> <Venue/City> <Year>
        """
        year = str(self.date.year) if self.date else ""

        if self.is_festival and self.band:
            return f"{self.band.name} {year}".strip()

        if self.tour_title and self.band:
            return f"{self.band.name} {self.tour_title} {year}".strip()

        loc = (self.venue.name if self.venue and self.venue.name
               else self.venue.city if self.venue and self.venue.city
               else self.venue.country if self.venue and self.venue.country
               else "")
        if self.band:
            return f"{self.band.name} {loc} {year}".strip()

        return f"{loc} {year}".strip()

# YouTube


User = get_user_model()


YOUTUBE_HOSTS = {
    "www.youtube.com", "youtube.com", "m.youtube.com",
    "youtu.be", "music.youtube.com"
}


def extract_youtube_id(url: str) -> str | None:
    """
    Accepts common YouTube URL forms:
      - https://www.youtube.com/watch?v=VIDEOID
      - https://youtu.be/VIDEOID
      - https://www.youtube.com/shorts/VIDEOID
      - https://www.youtube.com/embed/VIDEOID
    Returns just the VIDEOID or None if not recognized.
    """
    try:
        u = urlparse(url)
    except Exception:
        return None

    if u.netloc not in YOUTUBE_HOSTS:
        return None

    # youtu.be/<id>
    if u.netloc == "youtu.be":
        vid = u.path.lstrip("/")
        return vid if vid else None

    # /watch?v=<id>
    if u.path == "/watch":
        q = parse_qs(u.query)
        vid = q.get("v", [None])[0]
        return vid

    # /shorts/<id>
    m = re.match(r"^/shorts/([^/?#]+)", u.path)
    if m:
        return m.group(1)

    # /embed/<id>
    m = re.match(r"^/embed/([^/?#]+)", u.path)
    if m:
        return m.group(1)

    return None


class GigVideo(models.Model):
    gig = models.ForeignKey(
        "Gig", on_delete=models.CASCADE, related_name="videos")
    url = models.URLField(
        help_text="Paste a YouTube link (watch, youtu.be, shorts ok)")
    title = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-is_featured", "-added_at"]

    def clean(self):
        vid = extract_youtube_id(self.url or "")
        if not vid:
            raise ValidationError({
                "url": "Please provide a valid YouTube link."
            })

    @property
    def video_id(self) -> str | None:
        return extract_youtube_id(self.url or "")

    @property
    def embed_url(self) -> str | None:
        vid = self.video_id
        return (
            f"https://www.youtube-nocookie.com/embed/{vid}"
            if vid else None
        )

    @property
    def thumbnail_url(self) -> str | None:
        vid = self.video_id
        return (
            f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            if vid else None
        )

    def save(self, *args, **kwargs):
        # Ensure only one featured video per gig
        super().save(*args, **kwargs)
        if self.is_featured:
            GigVideo.objects.filter(gig=self.gig).exclude(
                pk=self.pk
            ).update(is_featured=False)

    def __str__(self):
        return self.title or (self.video_id or "YouTube Video")
