from django import forms
from .models import Item_account

class ItemAccountForm(forms.ModelForm):
    class Meta:
        model = Item_account
        fields = ['name']

class ItemAccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Item_account
        fields = ['name']