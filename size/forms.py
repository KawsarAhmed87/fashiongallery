from django import forms
from .models import Size

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']

class SizeUpdateForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']