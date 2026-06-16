---
name: accounts-templates
description: Patterns for account_list.html and account_form.html — summary cards, type badges, tfoot totals, breadcrumb header, tip box
metadata:
  type: project
---

## finance_filters templatetag location

`brl_currency` filter lives in `accounts/templatetags/finance_filters.py`. Load with `{% load finance_filters %}` at the top of any template that needs it. The `accounts` app is in INSTALLED_APPS as `'accounts'` so Django auto-discovers the templatetags package.

The filter uses `Decimal` for precision and formats as `R$ 1.234,56` (dot thousands, comma decimal). Handles None, zero, and negatives.

## Summary cards pattern (account_list)

Three-card grid above the table using context vars from `AccountListView.get_context_data`:
- `total_balance` — Sum of active accounts (via `aggregate(Sum('balance'))`)
- `active_count` — Count of active accounts
- `inactive_count` — Count of inactive accounts
- `grand_total` — Sum of ALL accounts (active + inactive), shown in tfoot

Card layout: `flex items-center gap-3`, icon in `bg-{color}/20 p-2 rounded-lg`, value in `text-2xl font-bold tabular-nums`.

## Type badge colors (accounts)

| account_type | badge classes |
|---|---|
| checking | `bg-blue-900/30 text-blue-400` |
| savings | `bg-violet-900/30 text-violet-400` |
| cash | `bg-amber-900/30 text-amber-400` |
| investment | `bg-emerald-900/30 text-emerald-400` |
| credit_card | `bg-rose-900/30 text-rose-400` |

Base: `text-xs px-2 py-0.5 rounded-full font-medium`

Same colors used for inline SVG icons in the Name column (icon lives inside `bg-gray-800 p-1.5 rounded-lg`).

## Table footer total

```html
<tfoot>
  <tr class="border-t border-gray-800 bg-gray-900/50">
    <td class="px-4 py-3 text-xs font-medium text-gray-400 uppercase tracking-wide" colspan="2">Total geral</td>
    <td class="px-4 py-3 text-gray-300 font-semibold tabular-nums">{{ grand_total|brl_currency }}</td>
    <td colspan="2"></td>
  </tr>
</tfoot>
```

## account_form header pattern

Breadcrumb + icon + title block above the form:
1. `<a>` breadcrumb with left-arrow SVG `w-3 h-3`, `text-gray-500 hover:text-gray-300 text-xs`
2. `flex items-center gap-4 mb-6 pb-6 border-b border-gray-800` wrapper
3. Icon circle: `bg-violet-600/20 p-3 rounded-xl` + `w-6 h-6 text-violet-400` SVG
4. Title `text-lg font-semibold text-gray-100` + subtitle `text-sm text-gray-400`

## Tip/info box pattern

```html
<div class="bg-gray-800/50 border border-gray-700 rounded-lg p-4 mt-5">
  <div class="flex items-start gap-2.5">
    <!-- lightbulb SVG w-4 h-4 text-violet-400 flex-shrink-0 mt-0.5 -->
    <div>
      <p class="text-violet-400 text-sm font-medium mb-1">Dica</p>
      <p class="text-gray-400 text-xs leading-relaxed">...</p>
    </div>
  </div>
</div>
```

## Empty state with type badges

The empty state includes a horizontal flex-wrap row of all type badges as a visual hint of what types are available, between the description and the CTA button.

## view changes needed for summary cards

`AccountListView.get_context_data` must import `from django.db.models import Sum` and compute `active_count`, `inactive_count`, `total_balance` (active only), `grand_total` (all accounts). Template does NOT calculate totals — always delegate to the view.
