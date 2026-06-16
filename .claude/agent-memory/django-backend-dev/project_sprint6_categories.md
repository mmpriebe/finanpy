---
name: sprint6-categories
description: Sprint 6 — Category model/admin/form/views/URLs done; mounted at categorias/; unique_together on (user, name, transaction_type)
metadata:
  type: project
---

Category app backend fully implemented in Sprint 6.

Key decisions:
- `unique_together = ('user', 'name', 'transaction_type')` — same name can exist for both income and expense categories, but not twice within the same type per user.
- `TRANSACTION_TYPES` choices: `('income', 'Receita')` and `('expense', 'Despesa')`.
- `CategoryToggleView` uses `get_object_or_404(Category, pk=pk, user=request.user)` — same pattern as `AccountToggleView`.
- `app_name = 'categories'`; mounted at `categorias/` in `core/urls.py`.
- Migration `categories/migrations/0001_initial.py` applied cleanly; 0 system-check issues.
- No `get_form_kwargs` needed — `CategoryForm` does not require user context (no user-scoped FK fields in the form).

**Why:** Standard user-isolated CRUD following the established accounts app pattern.

**How to apply:** When implementing transactions app, categories FK in the transaction form will need `get_form_kwargs` to pass user and filter categories by `user=request.user`.
