from django import forms
from .models import Product, Comment, Reply

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['sku']
        # fields = ['name', 'slug', 'category', 'tags', 'brand', 'size', 'colour', 'featured','price','discount_price','quantity']

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['sku']


class CommentForm(forms.Form):
    rating = forms.IntegerField()
    text = forms.CharField()

class ReplyForm(forms.Form):
    comment_id = forms.IntegerField()
    text = forms.CharField()

