from django import template
from django.utils import timezone

register = template.Library()

@register.inclusion_tag("gigs/_countdown_badge.html")
def countdown_badge(gig):
    """
    Simple backend-only countdown:
    - hides for past gigs
    - '🎵 Tonight!' on gig day
    - '⏳ 1–6d' within a week
    - '🔥 Xd' otherwise
    """
    if not getattr(gig, "date", None):
        return {"show": False}

    today = timezone.localdate()
    days = (gig.date - today).days

    if days < 0:
        return {"show": False}

    if days == 0:
        label = "🎵 Tonight!"
        css_class = "badge bg-danger"
    elif days < 7:
        label = f"⏳ {days}d"
        css_class = "badge bg-warning text-dark"
    else:
        label = f"🔥 {days}d"
        css_class = "badge bg-success"

    return {"show": True, "label": label, "css_class": css_class}
