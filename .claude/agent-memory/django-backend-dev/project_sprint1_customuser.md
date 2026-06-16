---
name: project-sprint1-customuser
description: Sprint 1 CustomUser implementation details — what was built, key decisions, and gotchas
metadata:
  type: project
---

Sprint 1 — CustomUser e Autenticação is implemented and migrations are clean.

**Key decisions made:**

- `CustomUser` inherits `AbstractUser` (not `AbstractBaseUser`) to preserve Django's built-in permission framework, password validation, and admin compatibility without re-implementing them.
- `username = None` on the class removes the username column from the DB schema (migration confirmed no username field).
- `RegisterView.success_url` uses the literal string `'/dashboard/'` instead of `reverse_lazy('core:dashboard')` because `core/views.py` and the dashboard URL don't exist until Sprint 4. This avoids a `NoReverseMatch` at import time.
- `LoginForm` inherits `AuthenticationForm` and adjusts the `username` field's `input_type` to `'email'` — Django's `AuthenticationForm` still uses `username` as the field name internally (it maps to `USERNAME_FIELD`), so the label and widget type are overridden in `__init__`.
- The SQLite DB was deleted and recreated from scratch because `admin.0001_initial` had already been applied against the default `auth.User` before `users.0001_initial` existed, causing `InconsistentMigrationHistory`.

**Files created/modified:**
- `users/models.py` — `CustomUserManager` + `CustomUser`
- `users/admin.py` — `CustomUserAdmin` with email-based fieldsets
- `users/apps.py` — added `default_auto_field`
- `users/forms.py` — `RegisterForm` + `LoginForm`
- `users/views.py` — `RegisterView`, `LoginView`, `LogoutView`
- `users/urls.py` — routes: `cadastro/`, `login/`, `logout/`
- `core/urls.py` — includes `users.urls` at root prefix `''`
- `users/migrations/0001_initial.py` — generated and applied

**Tasks 1.8.3 and 1.8.4** (createsuperuser + admin login verification) are interactive — must be done manually by the user.

**Why:** Standard Django custom user pattern. `AbstractUser` chosen over `AbstractBaseUser` for minimal boilerplate while still removing username.

**How to apply:** All future FKs to user must use `settings.AUTH_USER_MODEL`. Never use `'auth.User'`. The `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL` are set in settings — do not hardcode these paths in views.
