---
name: categories-templates
description: Categories list/form patterns — by_type filter for group splitting, per-group empty states, sidebar URL fix
metadata:
  type: project
---

## Categories template patterns (Sprint 6)

### by_type custom filter
DTL's `{% with %}` cannot accumulate values inside a loop (inner `{% with %}` doesn't modify outer scope). To split a queryset by field value in a template, the correct approach is a custom filter in `finance_filters.py`:

```python
@register.filter
def by_type(queryset, transaction_type):
    return [item for item in queryset if item.transaction_type == transaction_type]
```

Usage in template:
```html
{% load finance_filters %}
{% with income_list=categories|by_type:'income' %}
  {% if income_list %}...{% else %}...{% endif %}
{% endwith %}
```

This avoids the DTL variable scoping trap entirely and gives clean `{% if %}` / `{% else %}` branching.

### Category list structure
- Two sections: Receitas (emerald) and Despesas (rose)
- Section headers use colored icon + uppercase text (pattern from accounts)
- Each section shows its own table or an empty-state dashed card
- Global empty state (no categories at all) shows category examples as colored badges
- Inactive rows use `opacity-50` class on the `<tr>`
- Toggle button: rose destructive style when active (to deactivate), emerald when inactive (to activate)

### Sidebar fix
`base_authenticated.html` sidebar link for Categorias was using hardcoded `/categorias/` and `url_name == 'category-list'`. Corrected to:
- `href="{% url 'categories:list' %}"`
- Active detection: `request.resolver_match.app_name == 'categories'` (same pattern as accounts)

### Category form
- Same card layout as `account_form.html`: breadcrumb, icon header, novalidate, tip box
- Only two fields: `name` and `transaction_type`
- Dynamic title via `{% if object %}` (same as accounts)
- `transaction_type` renders as a `<select>` (widget set in CategoryForm)

### Tab system for category list (refactor)

The two stacked sections (Receitas / Despesas) were replaced with a tab UI. Key implementation notes:

- Both `income_list` and `expense_list` are computed in a single outer `{% with income_list=...|by_type:'income' expense_list=...|by_type:'expense' %}` so both counts are available for the tab badges without a second filter call.
- Tabs are `<button>` elements with `onclick="switchTab('income'|'expense')"`. The active tab uses `border-b-2 -mb-px` to overlap the `border-b border-gray-800` divider line and create the classic underline-tab look. `-mb-px` is the trick that makes the tab's bottom border sit exactly on the container's bottom border.
- Default state: income tab active (emerald classes), expense tab inactive (`text-gray-400 border-transparent hover:text-gray-200`).
- Panel visibility: `panel-income` starts visible, `panel-expense` starts with `hidden`. JS toggles `hidden` on panels and swaps class lists on buttons.
- Script lives in `{% block extra_js %}` as an IIFE. `window.switchTab` is exposed so inline `onclick` attributes can reach it. No Alpine.js, no htmx, pure vanilla JS.
- Global empty state renders instead of the entire tab UI when `categories` is falsy — the `{% with %}` block only runs inside the `{% if categories %}` branch.

**Why:** DTL scoping limitation means no flag variables inside loops — always reach for a custom filter when you need to branch on a filtered subset of a queryset.

**How to apply:** Any future list that needs per-type grouping should use `by_type` filter or a similar filter, not `{% with %}` flags. For tab UIs in other templates, follow the same `-mb-px` + `border-b-2` trick and IIFE pattern.
