from django import forms
from .models import Feed

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        # Django knows which model it has to take fields from
        fields = ['url','category']
        # Extracts that field from the specified model

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['category',]
