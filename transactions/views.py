from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.models import Account
from categories.models import Category
from transactions.forms import TransactionForm
from transactions.models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)

        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        account = self.request.GET.get('account')
        category = self.request.GET.get('category')

        if month:
            try:
                qs = qs.filter(date__month=int(month))
            except (ValueError, TypeError):
                pass

        if year:
            try:
                qs = qs.filter(date__year=int(year))
            except (ValueError, TypeError):
                pass

        if account:
            try:
                qs = qs.filter(account__pk=int(account))
            except (ValueError, TypeError):
                pass

        if category:
            try:
                qs = qs.filter(category__pk=int(category))
            except (ValueError, TypeError):
                pass

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(description__icontains=q)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['categories'] = Category.objects.filter(user=self.request.user)
        context['current_month'] = self.request.GET.get('month', '')
        context['current_year'] = self.request.GET.get('year', '')
        context['current_account'] = self.request.GET.get('account', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_q'] = self.request.GET.get('q', '')
        qs = self.get_queryset()
        context['income_count'] = qs.filter(transaction_type='income').count()
        context['expense_count'] = qs.filter(transaction_type='expense').count()
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def _is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self._is_ajax():
            form.save()
            messages.success(self.request, 'Transação criada com sucesso!')
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self._is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def _is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self._is_ajax():
            form.save()
            messages.success(self.request, 'Transação atualizada com sucesso!')
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self._is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Transação excluída com sucesso.')
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return HttpResponseRedirect(self.get_success_url())
