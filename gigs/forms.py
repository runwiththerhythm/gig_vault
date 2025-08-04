from django import forms
from dal import autocomplete
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Gig

class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['band', 'date', 'venue', 'status', 'notes', 'tour_title', 'other_artists', 'is_festival']
        widgets = {
            'band': autocomplete.ModelSelect2(url='band-autocomplete'),
            'venue': autocomplete.ModelSelect2(url='venue-autocomplete'),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': SummernoteWidget(),
            'other_artists': autocomplete.ModelSelect2Multiple(url='band-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('band'),
            HTML(
                '<small class="form-text text-muted">'
                'Can’t find the band? <a href="/bands/add/?next=/dashboard/gigs/new/">Add a new one</a>.'
                '</small>'
            ),
            Field('tour_title'),
            Field('other_artists'),
            Field('venue'),
            HTML(
                '<small class="form-text text-muted">'
                'Can’t find the venue? <a href="/venues/add/?next=/dashboard/gigs/new/">Add a new one</a>.'
                '</small>'
            ),
            Field('date'),
            Field('is_festival'),
            Field('status'),
            Field('notes'),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
