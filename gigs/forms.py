from django import forms
from dal import autocomplete
from django_summernote.widgets import SummernoteWidget
from .models import Gig, Band, Venue

class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['band', 'date', 'venue', 'status', 'notes', 'tour_title', 'other_artists', 'is_festival']
        widgets = {
            'band': autocomplete.ModelSelect2(url='band-autocomplete'),
            'venue': autocomplete.ModelSelect2(url='venue-autocomplete'),  # optional for later
            'notes': SummernoteWidget(),
            'other_artists': autocomplete.ModelSelect2Multiple(url='band-autocomplete'),

        }
