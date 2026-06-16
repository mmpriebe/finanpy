def finance_globals(request):
    if not request.user.is_authenticated:
        return {}
    try:
        from accounts.models import Account
        from categories.models import Category
        from core.views import _build_greeting
        return {
            'global_accounts': Account.objects.filter(user=request.user, is_active=True),
            'global_categories': Category.objects.filter(user=request.user, is_active=True),
            'greeting': _build_greeting(request.user),
        }
    except Exception:
        return {}
