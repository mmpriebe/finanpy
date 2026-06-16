---
name: landing-patterns
description: Approved patterns for the Finanpy landing page — navbar, hero, social proof, features, how-it-works, CTA, footer
metadata:
  type: project
---

## Navbar

Fixed glass: `fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-sm border-b border-gray-800`.
Max-width container: `max-w-6xl mx-auto px-6 h-16 flex items-center justify-between`.
Logo: `text-xl font-bold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent`.
"Entrar" button uses secondary style; "Cadastre-se" button uses primary gradient style.

## Hero

Section: `relative pt-32 pb-28 px-6 overflow-hidden`.
Background decorative radial gradient via inline `style=""` — no external images.
Subtle grid overlay also via inline `style=""` using `linear-gradient` lines.
Intro badge: `bg-violet-600/10 border border-violet-600/25 rounded-full px-4 py-1.5` with `w-1.5 h-1.5 rounded-full bg-violet-400` dot.
Headline: `text-5xl sm:text-6xl font-bold leading-tight mb-6 tracking-tight`.
  - Line 1 gradient: `bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent`.
  - Line 2: `text-gray-100`.
CTA row: `flex flex-col sm:flex-row items-center justify-center gap-4`, CTAs are `w-full sm:w-auto`.
Primary CTA shadow: `shadow-lg shadow-violet-900/40` added to hero primary button.
Micro-copy trust line: `text-gray-500 text-xs flex flex-wrap items-center justify-center gap-4` with check SVGs in `text-emerald-500`.
UI Mock panel: `bg-gray-900 border border-gray-800 rounded-2xl p-5 shadow-2xl shadow-black/50` — shows metric cards + mock transaction rows to illustrate the product without images.
Mock transaction rows: emerald up-arrow for income, rose down-arrow for expense — always maintains income/expense color convention.

## Social proof metrics bar

`bg-gray-900/50 border-y border-gray-800 py-12 px-6`.
Three stat items in `grid grid-cols-1 sm:grid-cols-3`.
Separator lines on center column in sm+: `absolute left-0/right-0 top-0 bottom-0 w-px bg-gray-800`.
Each stat: large gradient text label + `text-sm text-gray-400` subtitle.
Duplicate the center item in a `sm:hidden` block to avoid separator divs affecting mobile layout.

## Features section

`id="funcionalidades"` — anchor for "Ver funcionalidades" CTA scroll.
Six cards in `grid grid-cols-1 md:grid-cols-3 gap-5`.
Section header: overline `text-xs font-medium text-violet-400 uppercase tracking-widest mb-3`, then h2, then subtitle.
Card hover border varies by accent: `hover:border-violet-800/50`, `hover:border-indigo-800/50`, `hover:border-emerald-800/50`.
Icon container: `w-11 h-11 bg-{color}-600/15 rounded-xl` with `group-hover:bg-{color}-600/25 transition-colors duration-200`.
Icon size: `w-5 h-5`, Heroicons v2 outline, `stroke-width="1.5"`.
Feature pairs (violet/indigo/emerald): Contas Bancárias + Dashboard (violet), Categorias + Perfil (indigo), Transações + Dados Privados (emerald).

## Como funciona (3-step section)

`bg-gray-900/30` section background.
Grid: `grid grid-cols-1 md:grid-cols-3 gap-6 relative`.
Connecting line between steps (md+): `absolute top-8 left-1/3 right-1/3 h-px bg-gradient-to-r from-violet-600/40 to-indigo-600/40`.
Step number badge: `w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-900/40 relative z-10`.
Mobile: down-arrow SVG in `text-gray-700` shown between steps with `md:hidden`.

## CTA final section

Background via inline `style`: `linear-gradient(135deg, rgba(76,29,149,0.2) 0%, rgba(49,46,129,0.2) 100%)` with violet border.
Icon above headline: `w-14 h-14 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-2xl mx-auto mb-6 shadow-violet-900/50`.
Button: `inline-block` + `px-10 py-3.5` (larger than standard for the final CTA emphasis).
"Já tem conta? Entrar" link: `text-violet-400 hover:text-violet-300 transition-colors duration-150`.

## Footer

`border-t border-gray-800 bg-gray-900/50 py-8 px-6`.
`flex flex-col sm:flex-row items-center justify-between gap-4` — logo left, copyright right on sm+.
Logo in footer uses same gradient treatment as navbar.
Copyright: `text-gray-500 text-sm`, content: `© 2026 Finanpy. Todos os direitos reservados.`

**Why:** Full redesign of landing.html approved and applied 2026-06-14.
**How to apply:** Reuse these exact classes when rebuilding or extending the landing page, or building other public-facing marketing pages.

See also: [[project_template_structure]]
