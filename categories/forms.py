from django import forms

from categories.models import Category

INPUT_CLASSES = (
    'bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg '
    'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-500 '
    'focus:border-transparent transition-all duration-200'
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'transaction_type': forms.Select(attrs={'class': INPUT_CLASSES}),
        }
