from django import forms
from django.contrib.auth import get_user_model

from profiles.models import UserProfile

User = get_user_model()

_INPUT = (
    'bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg '
    'px-3 py-2.5 w-full placeholder-gray-600 focus:outline-none '
    'focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all duration-200'
)


class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': _INPUT}),
            'last_name':  forms.TextInput(attrs={'class': _INPUT}),
        }


class ProfilePersonalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '(00) 00000-0000'}),
        }


class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['zip_code', 'street', 'number', 'complement', 'neighborhood', 'city', 'state']
        widgets = {
            'zip_code':     forms.TextInput(attrs={'class': _INPUT, 'placeholder': '00000-000'}),
            'street':       forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Nome da rua'}),
            'number':       forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Nº'}),
            'complement':   forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Apto, bloco…'}),
            'neighborhood': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Bairro'}),
            'city':         forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Cidade'}),
            'state':        forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'UF', 'maxlength': '2'}),
        }
