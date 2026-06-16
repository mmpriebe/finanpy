---
name: project-profiles-app
description: UserProfile model, signal, forms, views, and URLs for the profiles app — key decisions and wiring notes
metadata:
  type: project
---

UserProfile app is fully implemented with a signal-driven 1:1 relationship to CustomUser.

**Key decisions:**

- `profiles/urls.py` has NO `app_name` (no namespace) — `base_authenticated.html` references `{% url 'profile-detail' %}` directly without a namespace prefix. Adding a namespace would break those links.
- Signal registered with `dispatch_uid='create_user_profile'` to prevent duplicate registration.
- `INSTALLED_APPS` uses `'profiles.apps.ProfilesConfig'` (not just `'profiles'`) so that `ProfilesConfig.ready()` fires and the signal is loaded.
- `ProfileUpdateView` is a plain `View` (not `UpdateView`) because it handles two forms simultaneously — `UserNameForm` (for `CustomUser`) and `ProfileForm` (for `UserProfile`). Both must be valid before either is saved.
- `ProfileDetailView.get_object` returns `self.request.user.profile` directly — no PK lookup needed since profile is 1:1.
- Signal uses `get_or_create` (not `create`) to be idempotent in case of data imports or management commands.

**Forms:**
- `ProfileForm` — `ModelForm` for `UserProfile`, field: `phone`
- `UserNameForm` — `ModelForm` for `CustomUser` (via `get_user_model()`), fields: `first_name`, `last_name`
- Both apply the project's standard input CSS via `_INPUT_CLASS` constant.

**URLs:**
- `/perfil/` → `profile-detail`
- `/perfil/editar/` → `profile-edit`

**Migration:** `profiles/migrations/0001_initial.py` — creates `UserProfile` table.

See also: [[project_sprint1_customuser]]
