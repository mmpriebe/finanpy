---
name: sprint3-auth-security
description: Sprint 3 auth security tasks — password reset, password change, django-axes, phone validator, delete protection
metadata:
  type: project
---

Sprint 3 authentication security tasks completed (AUTH-01, AUTH-02, AUTH-04, AUTH-05, AUTH-06).

**Why:** Production-blocking security features — rate limiting, password recovery, and protected delete operations.

**How to apply:** These are done; reference when extending auth flows or adding new delete views.

## AUTH-01 — Password Reset
- 4 URLs added to `users/urls.py` using Django's built-in `auth_views`
- Email backend configured in `core/settings.py` via env vars (console backend in dev)
- Text templates created: `templates/users/password_reset_email.txt`, `templates/users/password_reset_subject.txt`
- HTML templates (password_reset.html, done.html, confirm.html, complete.html) are frontend agent's responsibility

## AUTH-02 — Password Change via Profile
- `PasswordChangeView` added to `profiles/views.py` wrapping Django's `DjangoPasswordChangeView`
- `update_session_auth_hash` called in `form_valid` to keep user logged in after change
- URL `perfil/senha/` added to `profiles/urls.py` as `password-change`
- Note: `profiles/urls.py` has NO `app_name` — names are unnamespaced (e.g., `profile-detail`, not `profiles:profile-detail`)

## AUTH-04 — django-axes Rate Limiting
- Installed: `django-axes==8.3.1`
- `axes` added to `INSTALLED_APPS` after project apps
- `axes.middleware.AxesMiddleware` inserted at position 2 in MIDDLEWARE (after SecurityMiddleware, before WhiteNoise)
- Config: `AXES_FAILURE_LIMIT=5`, `AXES_COOLOFF_TIME=1` (hour), `AXES_RESET_ON_SUCCESS=True`
- `AUTHENTICATION_BACKENDS` set with `AxesStandaloneBackend` first, then `ModelBackend`
- Lockout template: `templates/users/lockout.html` (minimal, extends base.html)
- Migrations applied successfully (10 axes migrations)

## AUTH-05 — Phone Validator
- `_phone_validator` (RegexValidator) added to `profiles/forms.py`
- `ProfilePersonalForm.phone` declared as explicit `forms.CharField` with the validator
- Pattern: `^\(\d{2}\) \d{4,5}-\d{4}$`

## AUTH-06 — ProtectedError on Account/Category Delete
- `AccountDeleteView` added to `accounts/views.py` — catches `ProtectedError`, shows error message, redirects to list
- `CategoryDeleteView` added to `categories/views.py` — same pattern
- Import: `from django.db.models.deletion import ProtectedError` (NOT `from django.db import ProtectedError` — that raises ImportError)
- URLs added: `<int:pk>/excluir/` named `delete` in both apps
- Confirm-delete templates are frontend agent's responsibility
