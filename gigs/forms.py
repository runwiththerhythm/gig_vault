from django import forms
from dal import autocomplete
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div, Submit
from django.urls import reverse
from django.forms import inlineformset_factory

from .models import Gig, GigImage, GigVideo


class MultiFileClearableInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class GigForm(forms.ModelForm):

    class Meta:
        model = Gig
        fields = [
            "band", "tour_title", "other_artists",
            "date", "is_festival", "status", "notes",
        ]
        widgets = {
            "band": autocomplete.ModelSelect2(
                url="band-autocomplete",
                attrs={
                    "id": "band-field",
                    "data-placeholder": "Select a band...",
                    "data-allow-clear": "false",
                    "data-minimum-input-length": 1,
                },
            ),
            "other_artists": autocomplete.ModelSelect2Multiple(
                url="band-autocomplete",
                attrs={
                    "id": "supports-field",
                    "data-placeholder": "Add support/other artists…",
                    "data-minimum-input-length": 1,
                },
            ),
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "band" in self.initial:
            self.fields["band"].initial = self.initial["band"]

        band_add_url = reverse(
            "band_create") + "?next=" + reverse("gig_create")
        venue_add_url = reverse(
            "venue_create") + "?next=" + reverse("gig_create")

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field("band"),
            Field("tour_title"),
            Field("other_artists"),

            Div(
                Div(Field("date"), css_class="col-sm-4"),
                Div(Field("is_festival"),
                    css_class="col-sm-4 d-flex align-items-center mt-4"),
                Div(Field("status"), css_class="col-sm-4"),
                css_class="row g-3"
            ),
            Div("notes"),
        )


class GigImageForm(forms.ModelForm):
    class Meta:
        model = GigImage
        fields = ["image", "is_cover"]  # add 'caption' here if added to model


# Inline formset: one gig, multiple images
GigImageFormSet = inlineformset_factory(
    Gig,
    GigImage,
    form=GigImageForm,
    extra=0,
    can_delete=True
)


class GigVideoForm(forms.ModelForm):
    class Meta:
        model = GigVideo
        fields = ["url", "title", "is_featured"]
        widgets = {
            "url": forms.URLInput(attrs={
                "placeholder": "Paste a YouTube link"}),
            "title": forms.TextInput(attrs={
                "placeholder": "Optional title"}), }


GigVideoFormSet = inlineformset_factory(
    Gig,
    GigVideo,
    form=GigVideoForm,
    extra=1,
    can_delete=True
)
