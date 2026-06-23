from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

from profiles.forms import ProfileAddressForm, ProfilePersonalForm, UserNameForm
from profiles.models import UserProfile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'

    def get_object(self, queryset=None):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        return redirect('profile-detail')

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        tab = request.POST.get('tab', 'personal')

        name_form     = UserNameForm(request.POST, instance=request.user)
        personal_form = ProfilePersonalForm(request.POST, instance=profile)
        address_form  = ProfileAddressForm(request.POST, instance=profile)

        if tab == 'personal':
            forms_valid = name_form.is_valid() and personal_form.is_valid()
            if forms_valid:
                name_form.save()
                personal_form.save()
                user = request.user
                return JsonResponse({
                    'success': True,
                    'tab': 'personal',
                    'first_name': user.first_name,
                    'last_name':  user.last_name,
                    'full_name':  user.get_full_name(),
                    'phone':      profile.phone,
                })
            errors = {**name_form.errors, **personal_form.errors}
            return JsonResponse({'success': False, 'errors': {k: list(v) for k, v in errors.items()}}, status=400)

        if tab == 'address':
            if address_form.is_valid():
                address_form.save()
                p = profile
                return JsonResponse({
                    'success': True,
                    'tab': 'address',
                    'zip_code':     p.zip_code,
                    'street':       p.street,
                    'number':       p.number,
                    'complement':   p.complement,
                    'neighborhood': p.neighborhood,
                    'city':         p.city,
                    'state':        p.state,
                })
            return JsonResponse({'success': False, 'errors': {k: list(v) for k, v in address_form.errors.items()}}, status=400)

        return JsonResponse({'success': False, 'errors': {'__all__': ['Tab inválida.']}}, status=400)


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    template_name = 'profiles/password_change.html'
    success_url = reverse_lazy('profile-detail')

    def form_valid(self, response):
        messages.success(self.request, 'Senha alterada com sucesso.')
        update_session_auth_hash(self.request, self.request.user)
        return super().form_valid(response)
