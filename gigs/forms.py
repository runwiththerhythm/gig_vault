from django import forms
from dal import autocomplete
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Gig
from django.urls import reverse



class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['band', 'date', 'venue', 'status', 'notes', 'tour_title', 'other_artists', 'is_festival']
        widgets = {
            'band': autocomplete.ModelSelect2(url='band-autocomplete'),
            'venue': autocomplete.ModelSelect2(url='venue-autocomplete'),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'other_artists': autocomplete.ModelSelect2Multiple(url='band-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        band_add_url = reverse('band_create') + '?next=' + reverse('gig_create')
        venue_add_url = reverse('venue_create') + '?next=' + reverse('gig_create')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('band'),
            HTML(
                f'<small class="form-text text-muted">'
                f'Can’t find the band? <button type="button" class="btn btn-link p-0" data-bs-toggle="modal" data-bs-target="#addBandModal">Add a new one</button>.'
                '</small>'
            ),
            Field('tour_title'),
            Field('other_artists'),
            Field('venue'),
            HTML(
                f'<small class="form-text text-muted">'
                f'Can’t find the venue? <a href="{venue_add_url}">Add a new one</a>.'
                '</small>'
            ),
            Field('date'),
            Field('is_festival'),
            Field('status'),
            Div('notes'),
            Submit('submit', 'Save', css_class='btn btn-primary'),
        )
