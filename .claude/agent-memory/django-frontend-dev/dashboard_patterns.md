---
name: dashboard-patterns
description: Dashboard template patterns — metric cards grid, transactions table, empty state, floatformat usage without brl_currency filter
metadata:
  type: project
---

## Metric cards grid

Four metric cards use `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8`. Each card is `bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors duration-200`.

Card anatomy: icon (top-right, w-8 h-8 bg-gray-800 rounded-lg), label (`text-xs font-medium text-gray-400 uppercase tracking-wide`), value (`text-2xl font-bold tabular-nums`), sub-label (`text-xs text-gray-500 mt-1`).

Saldo Total card uses `text-gray-100` (neutral). Income card uses `text-emerald-400`. Expenses card uses `text-rose-400`. Monthly balance card conditionally picks color: `{% if monthly_balance >= 0 %}text-emerald-400{% else %}text-rose-400{% endif %}`.

## Currency display (without brl_currency filter)

When `brl_currency` templatetag is not yet available, use: `R$ {{ value|floatformat:2 }}`. Note: this does NOT produce thousand separators — it outputs `R$ 1234.56` not `R$ 1.234,56`. Once `brl_currency` filter is wired up, swap to `{{ value|brl_currency }}`.

## Transactions table section

Section header row: title (`text-base font-semibold text-gray-100`) + "Ver todas" link (`text-xs font-medium text-violet-400 hover:text-violet-300`) right-aligned. Table container: `bg-gray-900 border border-gray-800 rounded-xl overflow-hidden`. Columns: Data, Descrição, Categoria, Conta, Tipo, Valor.

Type badges: `inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400` (income) and `bg-rose-500/10 text-rose-400` (expense).

Value column: right-aligned, conditionally colored. Expenses prefixed with `-`: `{% if tx.transaction_type == 'expense' %}-{% endif %}R$ {{ tx.amount|floatformat:2 }}`.

Table footer: `border-t border-gray-800 px-4 py-3` with "Ver todas as transações →" link.

## Null-safe category/account

`{{ tx.category.name|default:"—" }}` and `{{ tx.account.name|default:"—" }}` handle None FK gracefully.

## Empty state

When `recent_transactions` is empty: `bg-gray-900 border border-gray-800 rounded-xl p-12 flex flex-col items-center justify-center text-center`. Icon in `w-14 h-14 bg-gray-800 rounded-full`. Title `text-gray-100 font-medium`, sub-text `text-gray-400 text-sm max-w-xs`, followed by primary gradient button linking to `/transacoes/nova/`.

## Hardcoded hrefs (temporary)

While transaction URLs are not registered, use href strings `/transacoes/` and `/transacoes/nova/` instead of `{% url 'transaction-list' %}` to avoid NoReverseMatch errors. Replace with named URL tags once URLs exist.

See also: [[project_template_structure]]
