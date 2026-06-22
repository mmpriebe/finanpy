from django import forms
from django.contrib.auth import get_user_model

from core.forms import INPUT_CLASS_PROFILE
from profiles.models import UserProfile

User = get_user_model()


class UserNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE}),
            'last_name':  forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE}),
        }


class ProfilePersonalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': '(00) 00000-0000'}),
        }


class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['zip_code', 'street', 'number', 'complement', 'neighborhood', 'city', 'state']
        widgets = {
            'zip_code':     forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': '00000-000'}),
            'street':       forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'Nome da rua'}),
            'number':       forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'Nº'}),
            'complement':   forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'Apto, bloco…'}),
            'neighborhood': forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'Bairro'}),
            'city':         forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'Cidade'}),
            'state':        forms.TextInput(attrs={'class': INPUT_CLASS_PROFILE, 'placeholder': 'UF', 'maxlength': '2'}),
        }
