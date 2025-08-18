# gigs/templatetags/gig_extras.py
from django import template
from django.utils import timezone

register = template.Library()

@register.inclusion_tag("gigs/_countdown_badge.html")
def countdown_badge(gig):
    """
    Backend-only countdown:
    - hides for past gigs
    - '🎵 Tonight!' on gig day
    - '⏳ 1–6d' within a week
    - '🔥 Xd' otherwise
    """
    date_val = getattr(gig, "date", None)
    if not date_val:
        return {"show": False}

    # If it's a DateTimeField, normalize to date
    gig_date = date_val.date() if hasattr(date_val, "date") else date_val
    today = timezone.localdate()

    # Ensure both are date objects
    if not hasattr(gig_date, "toordinal"):
        return {"show": False}

    days = (gig_date - today).days

    if days < 0:
        return {"show": False}
    if days == 0:
        return {"show": True, "label": "🎵 Tonight!", "css_class": "badge bg-danger"}
    if days < 7:
        return {"show": True, "label": f"⏳ {days}d", "css_class": "badge bg-warning text-dark"}
    return {"show": True, "label": f"🔥 {days}d", "css_class": "badge bg-success"}
