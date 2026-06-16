from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

_PT_MONTHS = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
]


def _build_greeting(user):
    hour = timezone.localtime().hour
    name = user.first_name or user.email.split('@')[0]

    if 5 <= hour < 12:
        return {
            'salutation': f'Bom dia, {name}!',
            'message': 'Planeje seus gastos antes de começar o dia — pequenas decisões fazem grande diferença.',
            'period': 'morning',
        }
    elif 12 <= hour < 18:
        return {
            'salutation': f'Boa tarde, {name}!',
            'message': 'Bom momento para registrar os lançamentos da manhã e manter o controle em dia.',
            'period': 'afternoon',
        }
    elif 18 <= hour < 24:
        return {
            'salutation': f'Boa noite, {name}!',
            'message': 'Revise os gastos do dia e encerre o dia sabendo exatamente onde está seu dinheiro.',
            'period': 'evening',
        }
    else:
        return {
            'salutation': f'Boa madrugada, {name}!',
            'message': 'Seus objetivos financeiros não dormem — que bom que você também está de olho neles.',
            'period': 'night',
        }

try:
    from accounts.models import Account
    from categories.models import Category
    from transactions.models import Transaction
    _finance_models_available = True
except ImportError:
    _finance_models_available = False


class LandingView(TemplateView):
    template_name = 'landing.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        today = date.today()

        if not _finance_models_available:
            context.update({
                'total_balance': 0,
                'monthly_income': 0,
                'monthly_expenses': 0,
                'monthly_balance': 0,
                'recent_transactions': [],
                'accounts': [],
                'categories': [],
                'greeting': _build_greeting(user),
                'current_month_label': f'{_PT_MONTHS[today.month - 1]} {today.year}',
                'savings_rate': 0,
                'top_expense_categories': [],
                'top_expense_max': 1,
            })
            return context

        total_balance = (
            Account.objects
            .filter(user=user, is_active=True)
            .aggregate(total=Sum('balance'))['total'] or 0
        )

        monthly_income = (
            Transaction.objects
            .filter(user=user, transaction_type='income', date__year=today.year, date__month=today.month)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        monthly_expenses = (
            Transaction.objects
            .filter(user=user, transaction_type='expense', date__year=today.year, date__month=today.month)
            .aggregate(total=Sum('amount'))['total'] or 0
        )

        recent_transactions = (
            Transaction.objects
            .filter(user=user)
            .order_by('-date', '-created_at')[:5]
        )

        top_expense_categories = list(
            Transaction.objects
            .filter(user=user, transaction_type='expense', date__year=today.year, date__month=today.month)
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:4]
        )
        top_expense_max = top_expense_categories[0]['total'] if top_expense_categories else 1

        savings_rate = 0
        if monthly_income > 0:
            savings_rate = max(0, min(100, int((1 - monthly_expenses / monthly_income) * 100)))

        context.update({
            'total_balance': total_balance,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_balance': monthly_income - monthly_expenses,
            'recent_transactions': recent_transactions,
            'accounts': Account.objects.filter(user=user, is_active=True),
            'categories': Category.objects.filter(user=user, is_active=True),
            'greeting': _build_greeting(user),
            'current_month_label': f'{_PT_MONTHS[today.month - 1]} {today.year}',
            'savings_rate': savings_rate,
            'top_expense_categories': top_expense_categories,
            'top_expense_max': top_expense_max,
        })
        return context
