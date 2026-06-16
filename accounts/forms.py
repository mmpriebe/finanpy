from django import forms

from accounts.models import Account

INPUT_CLASSES = (
    'bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg '
    'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-500 '
    'focus:border-transparent transition-all duration-200'
)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'account_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'balance': forms.NumberInput(attrs={'class': INPUT_CLASSES}),
        }
