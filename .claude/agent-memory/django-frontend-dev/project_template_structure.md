---
name: project-template-structure
description: Finanpy template structure, base templates, and key DTL patterns established in the project
metadata:
  type: project
---

Finanpy uses a two-base-template inheritance model:
- `base.html` — public pages (landing, login, register). HTML5 boilerplate, TailwindCSS CDN via `<script src="https://cdn.tailwindcss.com">`, blocks: `title`, `content`, `extra_head`, `extra_js`.
- `base_authenticated.html` — all logged-in pages. Extends `base.html`. Full sidebar + topbar layout. Adds blocks: `page_title` (topbar h1), `page_content` (main area).

The `base_authenticated.html` layout:
- Fixed sidebar (`w-64 bg-gray-900`) with logo, nav links, user info footer, logout link.
- Main content area (`ml-64`) with topbar (`h-16`) and scrollable content div (`p-6`).
- Django messages rendered inside content area before `page_content` block.

URL name pattern for sidebar active detection:
- `dashboard`, `account-list`, `category-list`, `transaction-list`, `profile-detail`

Active link class: `bg-violet-600/20 text-violet-400 font-medium rounded-lg`
Inactive link class: `text-gray-400 hover:text-gray-100 hover:bg-gray-800 rounded-lg`

User avatar: initials via `{{ request.user.first_name|first|upper }}{{ request.user.last_name|first|upper }}` inside gradient circle.

**Why:** Establishes the shell every authenticated page lives inside — sidebar, topbar, messages, content.
**How to apply:** All child templates extend `base_authenticated.html`, override `page_title` and `page_content`.
