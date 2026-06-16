---
name: auth-templates
description: Login and register template patterns — field rendering, error display, card layout for auth pages
metadata:
  type: project
---

## Auth page layout

Both login and register extend `base.html` (not base_authenticated). Outer wrapper: `min-h-screen flex items-center justify-center px-4`. Register adds `py-12` to avoid clipping on short viewports when the card is taller.

Card: `bg-gray-900 border border-gray-800 rounded-2xl p-8 w-full max-w-sm shadow-xl`

Logo block at top of card (centered):
```html
<span class="font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent text-2xl">Finanpy</span>
<p class="text-gray-400 text-sm mt-1">Entre na sua conta</p>
```

## Field rendering approach

`LoginForm` and `RegisterForm` have no custom widget classes. Render fields manually using `form.field_name.html_name`, `form.field_name.id_for_label`, and `form.field_name.value` — do NOT call `{{ field }}` directly (would render unstyled Django widget HTML).

- `LoginForm`: fields are `username` (input_type patched to `email` in __init__) and `password`
- `RegisterForm` fields: `first_name`, `last_name`, `email`, `password1`, `password2`

## Error display

Non-field errors (e.g. "wrong credentials"): `bg-rose-500/10 border border-rose-500/20 rounded-lg px-3 py-2 text-rose-400 text-xs` block above the form fields.

Per-field errors: `<p class="text-rose-400 text-xs mt-1">{{ form.field.errors|join:", " }}</p>`. For password fields with multiple validators, iterate `{% for error in form.passwordN.errors %}` instead of join.

Border highlight on error: add `{% if form.field.errors %}border-rose-500{% endif %}` inside the input's class attribute.

## Register layout detail

Nome and Sobrenome sit in a `grid grid-cols-2 gap-3` row to save vertical space. E-mail, password1, password2 each take a full row. All fields inside `<div class="space-y-5">`.

## Form attributes

All auth forms use `novalidate` on the `<form>` tag so Django controls validation, not the browser.

Password fields never repopulate value (type="password", no value attribute).

## Links between pages

Login → register: `/cadastro/`  Register → login: `/login/`
Both links: `text-violet-400 hover:text-violet-300 transition-colors duration-150`

See [[project_template_structure]] for URL names.
