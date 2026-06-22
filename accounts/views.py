from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from accounts.forms import AccountForm
from accounts.models import Account
from core.mixins import AjaxFormMixin


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list
        active_qs = qs.filter(is_active=True)
        context['active_count'] = active_qs.count()
        context['inactive_count'] = qs.filter(is_active=False).count()
        context['total_balance'] = active_qs.aggregate(total=Sum('balance'))['total'] or 0
        context['grand_total'] = qs.aggregate(total=Sum('balance'))['total'] or 0
        return context


class AccountCreateView(AjaxFormMixin, LoginRequiredMixin, CreateView):
    form_class = AccountForm
    template_name = 'accounts/account_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self._is_ajax():
            form.save()
            return self.ajax_success('Conta criada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:list')


class AccountUpdateView(AjaxFormMixin, LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if self._is_ajax():
            form.save()
            return self.ajax_success('Conta atualizada com sucesso!')
        return super().form_valid(form)


class AccountToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        account.is_active = not account.is_active
        account.save()
        messages.success(request, 'Status da conta atualizado.')
        return redirect('accounts:list')
