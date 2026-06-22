from django import forms

from accounts.models import Account
from core.forms import INPUT_CLASS


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'account_type': forms.Select(attrs={'class': INPUT_CLASS}),
            'balance': forms.NumberInput(attrs={'class': INPUT_CLASS}),
        }
