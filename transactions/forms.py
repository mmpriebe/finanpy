from django import forms

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction

INPUT_CLASS = (
    'bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg '
    'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-violet-500 '
    'focus:border-transparent transition-all duration-200 w-full'
)


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
            field.widget.attrs['class'] = INPUT_CLASS

    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'transaction_type', 'date', 'account', 'category', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
