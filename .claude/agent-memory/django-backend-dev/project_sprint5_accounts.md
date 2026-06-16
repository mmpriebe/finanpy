---
name: project-sprint5-accounts
description: Sprint 5 — Account model, admin, forms, views, URLs fully implemented; accounts already in INSTALLED_APPS from the start
metadata:
  type: project
---

Sprint 5 delivered the full `accounts` app backend.

**Key decisions:**
- `accounts` was already registered in `INSTALLED_APPS` as plain `'accounts'` (not via AppConfig path) — no change needed.
- `AccountToggleView` uses base `View` + `post()` method with `get_object_or_404(Account, pk=pk, user=request.user)` for data isolation on the toggle action (no suitable CBV for a simple field-flip redirect).
- `AccountUpdateView.success_url` uses `reverse_lazy('accounts:list')` at class level; `AccountCreateView` uses `get_success_url()` returning `reverse_lazy(...)` — both patterns are valid, class-level attribute is preferred when no dynamic data is needed.
- `AccountForm` stores widget CSS classes in a module-level `INPUT_CLASSES` constant to avoid repetition across fields.
- Migration `accounts/migrations/0001_initial.py` applied cleanly; `django.manage.py check` reports 0 issues.

**URL namespace:** `app_name = 'accounts'`, mounted at `contas/` in `core/urls.py`.

**ACCOUNT_TYPES choices:** checking, savings, cash, investment, credit_card.

See [[project-sprint1-customuser]], [[project-profiles-app]].
