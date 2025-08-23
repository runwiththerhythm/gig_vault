from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from django.test import TestCase
from django.urls import reverse

from .models import Band, Venue, Gig, GigVideo, GigImage


# ---------- Helpers that adapt to your current Venue schema ----------

def venue_field_map():
    """Return a dict mapping logical keys -> actual Venue field names."""
    fields = {
        f.name
        for f in Venue._meta.get_fields()
        if getattr(f, "concrete", False)
    }

    def pick(*candidates):
        for c in candidates:
            if c in fields:
                return c
        return None

    return {
        "name": pick("venue_name", "name"),
        "city": pick("venue_city", "city"),
        "country": pick("venue_country", "country"),
        "address_text": pick("address_text"),
    }


def make_venue(
    name="O2 Arena",
    city="London",
    country="UK",
    address_text=None
):
    fm = venue_field_map()
    data = {}
    if fm["name"]:
        data[fm["name"]] = name
    if fm["city"]:
        data[fm["city"]] = city
    if fm["country"]:
        data[fm["country"]] = country
    if fm["address_text"] and address_text:
        data[fm["address_text"]] = address_text
    return Venue.objects.create(**data)


def venue_str_contains(v, substrings):
    """Robust check across different __str__ formats."""
    s = str(v)
    return all(sub in s for sub in substrings)


# ------------------------------ Tests -------------------------------

class BandModelTests(TestCase):
    def test_str_returns_name(self):
        band = Band.objects.create(name="Iron Maiden")
        self.assertEqual(str(band), "Iron Maiden")


class VenueModelTests(TestCase):
    def test_str_contains_key_parts(self):
        v = make_venue(name="O2 Arena", city="London", country="UK")
        self.assertTrue(venue_str_contains(v, ["O2 Arena", "London"]))


class GigModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.band = Band.objects.create(name="Metallica")
        self.venue = make_venue(
            name="Download Festival", city="Donington", country="UK")

    def test_create_gig_minimal(self):
        g = Gig.objects.create(
            user=self.user,
            band=self.band,
            venue=self.venue,
            date=date.today() + timedelta(days=7),
            # don't set status explicitly in case your choices differ
        )
        self.assertEqual(g.band.name, "Metallica")
        self.assertEqual(str(g.venue).lower().startswith("download"), True)
        self.assertFalse(getattr(g, "is_festival", False))

    def test_other_artists_many_to_many(self):
        g = Gig.objects.create(
            user=self.user,
            band=self.band,
            venue=self.venue,
            date=date.today(),
        )
        support1 = Band.objects.create(name="Gojira")
        support2 = Band.objects.create(name="Mastodon")
        g.other_artists.add(support1, support2)
        self.assertEqual(g.other_artists.count(), 2)


class GigViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.client.login(username="tester", password="pw")

        self.band_up = Band.objects.create(name="Muse")
        self.band_att = Band.objects.create(name="Radiohead")

        self.venue = make_venue(
            name="Wembley Stadium", city="London", country="UK")

        # Upcoming gig (future date)
        self.gig_upcoming = Gig.objects.create(
            user=self.user,
            band=self.band_up,
            venue=self.venue,
            date=date.today() + timedelta(days=10),
        )
        # Attended gig (past date)
        self.gig_attended = Gig.objects.create(
            user=self.user,
            band=self.band_att,
            venue=self.venue,
            date=date.today() - timedelta(days=30),
        )

    def test_my_gigs_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse("my_gigs"))
        self.assertIn(resp.status_code, (302, 301))  # redirect to login

    def test_my_gigs_lists_user_gigs(self):
        resp = self.client.get(reverse("my_gigs"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Muse")
        self.assertContains(resp, "Radiohead")

    def test_gig_detail_renders(self):
        resp = self.client.get(
            reverse("gig_detail", args=[self.gig_upcoming.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Wembley")


class GigVideoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.band = Band.objects.create(name="Slipknot")
        self.venue = make_venue(
            name="AO Arena", city="Manchester", country="UK")
        self.gig = Gig.objects.create(
            user=self.user,
            band=self.band,
            venue=self.venue,
            date=date.today(),
        )

    def test_clean_rejects_invalid_youtube_url(self):
        v = GigVideo(gig=self.gig, url="https://example.com/not-youtube")
        with self.assertRaises(ValidationError):
            v.clean()

    def test_embed_url_property_for_valid_youtube(self):
        v = GigVideo.objects.create(
            gig=self.gig,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        self.assertIsNotNone(v.video_id)
        self.assertIn("youtube-nocookie.com/embed", v.embed_url or "")


class GigImageConstraintTests(TestCase):
    """
    Optional: Only runs if you have a DB-level constraint like:
        UniqueConstraint(
            fields=['gig'],
            condition=Q(is_cover=True),
            name='unique_cover_per_gig',
        )
    If not present, we SKIP this test.
    """
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.band = Band.objects.create(name="Deftones")
        self.venue = make_venue(name="Roundhouse", city="London", country="UK")
        self.gig = Gig.objects.create(
            user=self.user,
            band=self.band,
            venue=self.venue,
            date=date.today(),
        )

    def _has_unique_cover_constraint(self) -> bool:
        try:
            with connection.cursor() as cur:
                cur.execute("""
                    SELECT conname
                    FROM pg_constraint
                    WHERE conname = 'unique_cover_per_gig'
                """)
                return cur.fetchone() is not None
        except Exception:
            # e.g., SQLite in tests doesn't have pg_constraint
            return False

    def test_only_one_cover_image_allowed(self):
        if not self._has_unique_cover_constraint():
            self.skipTest(
                "Skipping: 'unique_cover_per_gig' constraint not found.")

        GigImage.objects.create(
            gig=self.gig,
            user=self.user,
            image="placeholder",
            is_cover=True,
        )

        with self.assertRaises(IntegrityError):
            GigImage.objects.create(
                gig=self.gig,
                user=self.user,
                image="placeholder-2",
                is_cover=True,
            )
