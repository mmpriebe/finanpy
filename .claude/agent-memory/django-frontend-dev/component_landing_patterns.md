---
name: component-landing-patterns
description: Landing page structure and reusable public-page component patterns established in Finanpy
metadata:
  type: project
---

## Landing page structure (templates/landing.html)

Three-section layout inside `{% block content %}`:
1. `<nav>` — sticky navbar, `bg-gray-950 border-b border-gray-800`, `sticky top-0 z-50`, `max-w-6xl mx-auto px-6 h-16`.
2. `<section class="py-24 px-6">` — hero with centered H1 (gradient span), `text-lg text-gray-400` subtitle, two CTA buttons side-by-side via `flex gap-4`.
3. `<section class="py-16 px-6">` — feature grid, `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6`.
4. `<footer class="bg-gray-900 border-t border-gray-800">` — copyright, `text-gray-500 text-sm`.

## Feature card pattern

```html
<div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
  <div class="bg-gradient-to-br from-violet-600/20 to-indigo-600/20 rounded-lg p-2 w-fit mb-4">
    <svg class="w-6 h-6 text-violet-400" ...>...</svg>
  </div>
  <h3 class="text-gray-100 font-semibold mb-2">Título</h3>
  <p class="text-gray-400 text-sm leading-relaxed">Descrição.</p>
</div>
```

Icon container: `bg-gradient-to-br from-violet-600/20 to-indigo-600/20 rounded-lg p-2 w-fit` — `w-fit` is key to keep it icon-sized.

## Hero CTA sizing

Public page CTAs use `px-6 py-3` (slightly larger than the standard `px-4 py-2` used in forms/tables) to give the hero visual weight.

## Navbar logo

```html
<span class="font-bold text-xl bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
  Finanpy
</span>
```

## Related

See [[project-template-structure]] for base template block names and authenticated layout.
