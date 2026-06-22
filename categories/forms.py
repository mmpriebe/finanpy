from django import forms

from categories.models import Category
from core.forms import INPUT_CLASS


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'transaction_type': forms.Select(attrs={'class': INPUT_CLASS}),
        }
