from django import forms
from .models import Colour

class ColourForm(forms.ModelForm):
    class Meta:
        model = Colour
        fields = ['name']

class ColourUpdateForm(forms.ModelForm):
    class Meta:
        model = Colour
        fields = ['name']