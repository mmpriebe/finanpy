---
name: dashboard-fix-findings
description: Findings from QA session verifying dashboard fixes — login/register templates created, sidebar hrefs fixed; what passed and what is still broken
metadata:
  type: project
---

After applying three fixes (base_authenticated.html sidebar hrefs changed to fixed paths, login.html and register.html templates created), the following was confirmed on 2026-06-14:

## Confirmed Working

- `/login/` returns 200 with correct form (email + password fields, violet-gradient button, design system compliant)
- `/cadastro/` returns 200 with correct form (first_name, last_name, email, password1, password2, 2-column grid layout)
- Registration POST with valid data returns 302 redirect to `/dashboard/` — user session created correctly
- `/dashboard/` returns 200 with full authenticated layout including sidebar, 4 metric cards (Saldo Total, Receitas do Mês, Despesas do Mês, Saldo Líquido), and empty state for Últimas Transações
- Sidebar active link highlighting works: Dashboard link shows `bg-violet-600/20 text-violet-400` when on dashboard, Perfil link when on /perfil/
- Sidebar footer shows user initials avatar (TQ), full name (Teste QA), and email (qa@finanpy.com)
- Logout POST to `/logout/` returns 302 redirect to `/` (landing page) — session destroyed correctly
- After logout, `/dashboard/` returns 302 redirect to `/login/?next=/dashboard/` — protected route working
- Login with invalid credentials returns 200 with error message styled in `text-rose-400 bg-rose-500/10 border border-rose-500/20`
- `/perfil/` returns 200 with profile card showing name, email, phone (Não informado), member since date in DD/MM/AAAA format
- Design system compliance: bg-gray-950 body, bg-gray-900 cards/sidebar, violet gradient logo, emerald for receitas, rose for despesas

## Known Broken

- `/contas/` returns 404 — accounts app URLs not yet registered in core/urls.py
- `/categorias/` returns 404 — categories app URLs not yet registered in core/urls.py
- `/transacoes/` returns 404 — transactions app URLs not yet registered in core/urls.py
- The sidebar links to /contas/, /categorias/, /transacoes/ are hardcoded hrefs that point to non-existent routes. The sprint 3 fix was correct for avoiding NoReverseMatch, but the underlying apps are not yet wired up.

## Test User

Credentials confirmed working: email=qa@finanpy.com, password=TesteSenha123!
(May be cleared if DB is reset)

**Why:** Verifying that template creation and sidebar href fixes resolved the 500 errors seen before this session.
**How to apply:** In future sessions, skip testing /contas/, /categorias/, /transacoes/ until those apps are registered in core/urls.py. Focus on auth + dashboard + profile flows which are confirmed working.
