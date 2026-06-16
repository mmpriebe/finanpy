---
name: sprint3-profile-qa-findings
description: QA findings from Sprint 3 and Sprint 4 verification — missing templates, broken URL names, no UserProfile for superuser
metadata:
  type: project
---

Sprint 3 profile flow QA session (2026-06-14) and Sprint 4 dashboard investigation (2026-06-14) revealed the following non-obvious issues:

**Why:** The profiles and dashboard backends are implemented but depend on templates and apps (accounts, categories, transactions) that do not yet exist. The sidebar in `base_authenticated.html` references URL names that have no registered routes.

**How to apply:** When testing, expect 500 errors on any page that extends `base_authenticated.html` because the sidebar references `{% url 'account-list' %}`, `{% url 'category-list' %}`, and `{% url 'transaction-list' %}` — none of which resolve until sprints 5/6/7 are implemented. These unresolvable URL names block ALL authenticated pages from rendering.

## Confirmed issues (as of Sprint 4)

1. `templates/users/login.html` is missing — `/login/` returns HTTP 500 (`TemplateDoesNotExist: users/login.html`). Confirmed live via curl.

2. `templates/users/register.html` is missing — `/cadastro/` returns HTTP 500 (`TemplateDoesNotExist: users/register.html`). Confirmed live via curl.

3. `base_authenticated.html` sidebar references 3 unresolvable URL names: `account-list`, `category-list`, `transaction-list`. These apps/views are not yet implemented (Sprints 5, 6, 7). Any authenticated page that extends this base — including `/dashboard/` and `/perfil/` — will raise `NoReverseMatch` at render time.

4. The `{% url 'users:logout' %}` in `base_authenticated.html` uses the namespaced form (`users:logout`) which IS correct — `users/urls.py` has `app_name = 'users'`. This is not a bug.

5. Superuser `marciano.priebe@gmail.com` has no associated `UserProfile` because the superuser was created before profiles migration was applied. The `post_save` signal never fired.

6. The superuser password is NOT `admin` — admin login via POST returns 200 (wrong credentials). Password is unknown; cannot authenticate via UI or admin panel without reset.

## Confirmed working (code review)

- `core/views.py`: `DashboardView` uses `LoginRequiredMixin` correctly. The `try/except ImportError` guard for `accounts` and `transactions` models is correct — when those apps don't exist, dashboard context defaults to zeros. **The view logic itself is not the problem.**
- `core/urls.py`: `dashboard/` route registered with name `dashboard`. Redirect to `/login/?next=/dashboard/` confirmed (302) when unauthenticated.
- `dashboard.html`: extends `base_authenticated.html`. Template logic is correct — the NoReverseMatch will be raised in `base_authenticated.html`, not in `dashboard.html` itself.
- `profiles/signals.py`, `profiles/apps.py`, `profiles/forms.py`, `profiles/urls.py` — correct.
- URL name `users:logout` is correctly namespaced in `base_authenticated.html`.
- `LOGIN_URL = '/login/'`, `LOGIN_REDIRECT_URL = '/dashboard/'`, `LOGOUT_REDIRECT_URL = '/'` are set correctly.
- `profiles/migrations/0001_initial.py` is applied.

## Blocking chain for accessing /dashboard/

The sequence of blocks is:
1. No `templates/users/login.html` → cannot log in via UI
2. No `accounts`, `categories`, `transactions` URL registrations → `base_authenticated.html` raises `NoReverseMatch` on render
3. Even if authentication is bypassed, `/dashboard/` would fail at step 2

## Test credentials in DB

- Superuser: `marciano.priebe@gmail.com` — password unknown (not `admin`). No UserProfile record.
