---
name: transactions-templates
description: Transaction list, form, and confirm-delete template patterns for Finanpy
metadata:
  type: project
---

Three templates created at `templates/transactions/`:

**transaction_list.html**
- Filter bar renders as a `bg-gray-900 border border-gray-800 rounded-xl p-4` card above the table.
- Filter selects use `flex-1 min-w-[...]` to wrap naturally at narrow viewports.
- Account/category select options pre-select with `{% if current_account == account.pk|stringformat:'s' %}selected{% endif %}` — converting pk to string for comparison against the string context variable.
- Income/expense badge: `bg-emerald-900/30 text-emerald-400` / `bg-rose-900/30 text-rose-400` with `inline-flex items-center text-xs px-2 py-0.5 rounded-full font-medium`.
- Amount column prefixes `+` for income, `-` for expense, then applies color via conditional class on the `<td>`.
- Empty state has two messages: one for active filters (suggest clearing), one for fresh state (invite to create). Empty state CTA now uses `onclick="openTransactionModal()"` button instead of `<a href>`.
- "Nova Transação" header button converted from `<a href>` to `<button onclick="openTransactionModal()">`.
- "Editar" row button converted from `<a href>` to `<button onclick="openEditTransactionModal(this)">` with `data-pk`, `data-description`, `data-amount`, `data-transaction-type`, `data-date`, `data-account`, `data-category`, `data-notes`, `data-url` attributes. Date passed as `Y-m-d` format for the date input.
- "Excluir" remains as `<a href>` link to confirm-delete page.
- Modal "Nova Transação" (IDs: `tx-modal`, `tx-modal-card`, `tx-create-form`) and Modal "Editar Transação" (IDs: `tx-edit-modal`, `tx-edit-modal-card`, `tx-edit-form`) follow exact category_list.html modal pattern.
- Modal form layout: `grid grid-cols-2 gap-4` inside `px-6 py-6`. Descrição, Categoria, Observações are `col-span-2`; Valor+Tipo and Data+Conta each occupy one column.
- Error IDs (create): `error-tx-description`, `error-tx-amount`, `error-tx-transaction-type`, `error-tx-date`, `error-tx-account`, `error-tx-category`, `error-tx-general`.
- Error IDs (edit): same but prefixed `edit-` instead of no prefix.
- JS IIFE for edit modal: `openEditTransactionModal(btn)` reads all `btn.dataset.*` values and sets `form.dataset.updateUrl = btn.dataset.url`. `data-transaction-type` maps to `btn.dataset.transactionType` (camelCase auto-conversion by the browser).
- Error field→ID mapping: field name `transaction_type` maps to error ID suffix `transaction-type` (underscores replaced with hyphens via `field.replace(/_/g, '-')`).
- Both modals use `window.openTransactionModal`, `window.closeTransactionModal`, `window.openEditTransactionModal`, `window.closeEditTransactionModal`.

**transaction_form.html**
- `max-w-2xl mx-auto` wrapper.
- Grid `grid grid-cols-2 gap-5` with `col-span-2` on description, category, and notes.
- `{{ form.FIELD }}` widget rendering — widgets must have Tailwind classes applied in forms.py.
- Non-field errors rendered in a `bg-rose-500/10 border border-rose-500/20` alert box below the grid.

**transaction_confirm_delete.html**
- `max-w-md mx-auto` wrapper.
- Destructive confirm button: `bg-rose-600 hover:bg-rose-500` (solid, not transparent like the list's delete action).
- Details card: `bg-gray-800/50 border border-gray-700` with dividers between rows.
- Warning pill: `bg-rose-500/10 border border-rose-500/20` with alert SVG icon.

**Sidebar fix applied in base_authenticated.html**
- Changed `/transacoes/` hardcoded href to `{% url 'transactions:list' %}`.
- Changed active detection from `url_name == 'transaction-list'` to `app_name == 'transactions'` (matches the accounts/categories pattern).
