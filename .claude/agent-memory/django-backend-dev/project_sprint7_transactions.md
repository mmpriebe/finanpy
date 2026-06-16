---
name: sprint7-transactions
description: Transaction model/admin/form/views/URLs done; FKs to Account and Category with PROTECT; mounted at transacoes/; 0 system-check issues
metadata:
  type: project
---

Transaction app fully implemented in Sprint 7.

**Model key decisions:**
- `account` FK uses `on_delete=PROTECT` (not CASCADE) — prevents accidental deletion of accounts that have transactions
- `category` FK uses `on_delete=PROTECT` for same reason
- `Meta.ordering = ['-date', '-created_at']` — newest first, tie-broken by creation time
- `TRANSACTION_TYPES` mirrors the same choices defined in `categories.Category.TRANSACTION_TYPES`

**Form pattern:**
- `TransactionForm.__init__` pops `user` kwarg before `super().__init__`, then filters both `account` and `category` querysets to active records owned by that user
- All widget classes set in a loop after `super().__init__` — the `date` widget uses `forms.DateInput(attrs={'type': 'date'})` declared in `Meta.widgets`, and the loop adds the CSS class on top
- `INPUT_CLASS` constant defined at module level to avoid repetition

**Views:**
- `TransactionListView.get_queryset` applies four optional GET filters: `month`, `year`, `account` (pk), `category` (pk) — each wrapped in try/except for invalid integer input
- `TransactionCreateView` uses `get_form_kwargs` to inject user, and `form_valid` to stamp `form.instance.user`
- `TransactionUpdateView` overrides both `get_queryset` (data isolation) and `get_form_kwargs` (user-scoped dropdowns)
- `TransactionDeleteView` overrides `get_queryset` only — no form involved

**URLs:**
- `app_name = 'transactions'`
- Mounted at `transacoes/` in `core/urls.py`
- Names: `transactions:list`, `transactions:create`, `transactions:update`, `transactions:delete`

**Migration:** `transactions/migrations/0001_initial.py` — applied cleanly, 0 system-check issues.

**Related:** [[sprint5-accounts]], [[sprint6-categories]]
