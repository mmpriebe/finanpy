from django import forms

from accounts.models import Account
from categories.models import Category
from core.forms import INPUT_CLASS
from transactions.models import Transaction

_INPUT_CLASS = f'{INPUT_CLASS} w-full'


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['account'].queryset = Account.objects.filter(
                user=self.user, is_active=True
            )
            self.fields['category'].queryset = Category.objects.filter(
                user=self.user, is_active=True
            )

        for field in self.fields.values():
            field.widget.attrs['class'] = _INPUT_CLASS

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'transaction_type', 'date', 'account', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
