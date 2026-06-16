---
name: profile-templates
description: Patterns established in profile_detail.html and profile_edit.html — avatar sizing, two-form edit page, field rendering without Django widget HTML
metadata:
  type: project
---

Profile templates live in `templates/profiles/`. Both extend `base_authenticated.html`, override `page_title` and `page_content`. Max-width container is `max-w-2xl` for detail/edit pages.

## profile_detail.html patterns

- Large avatar (w-16 h-16, text-xl) with gradient `from-violet-500 to-indigo-600` placed in a flex row alongside name/email.
- Name: `text-xl font-semibold text-gray-100` via `object.user.get_full_name`.
- Email: `text-sm text-gray-400`.
- Info grid uses `grid grid-cols-1 sm:grid-cols-2 gap-6`.
- Each info cell: label as `text-xs font-medium text-gray-400 uppercase tracking-wide mb-1`, value as `text-sm text-gray-100`.
- Empty phone fallback: `text-sm text-gray-500 italic` with "Não informado".
- Member-since date: `object.user.created_at|date:"d/m/Y"` — note field is on `CustomUser`, not `UserProfile`.
- Sections separated by `border-t border-gray-800 my-6`.
- Edit button: inline-block primary gradient `<a>` tag below the grid.

## profile_edit.html patterns

- Two separate form objects in context: `name_form` (first_name, last_name) and `profile_form` (phone).
- Both are submitted in a single `<form method="post">` — only one `{% csrf_token %}`.
- Fields rendered manually (not `{{ form.as_p }}`) to control input classes precisely.
- Input attributes accessed via: `id="{{ field.id_for_label }}"`, `name="{{ field.html_name }}"`, `value="{{ field.value|default:'' }}"`.
- Errors rendered with `{% for error in field.errors %}<p class="text-rose-400 text-xs mt-1">{{ error }}</p>{% endfor %}`.
- Section headings: `text-sm font-semibold text-gray-100 uppercase tracking-wide mb-4`.
- Name fields in `grid grid-cols-1 sm:grid-cols-2 gap-4`.
- Cancel link: `text-gray-400 hover:text-gray-100 text-sm transition-colors duration-150` pointing to `profile-detail`.

**Why:** Established when implementing sprint 3.7 profile feature. Manual field rendering avoids Django's default widget HTML interfering with Tailwind classes.
**How to apply:** Reuse the manual field rendering pattern for any form where widget styling needs full control. See [[project-template-structure]] for base template blocks.
