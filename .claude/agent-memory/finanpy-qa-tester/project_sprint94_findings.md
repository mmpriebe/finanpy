---
name: project-sprint94-findings
description: Sprint 9.4 visual QA findings — mobile responsiveness, design consistency, empty states, Django messages, sidebar nav
metadata:
  type: project
---

Sprint 9.4 QA executada em 2026-06-16 via análise estática (Playwright MCP indisponível no subagente). Todos os problemas verificados contra arquivos reais do projeto.

## Resultados por subtarefa

| Subtarefa | Status | Bloqueador? |
|---|---|---|
| 9.4.1 Responsividade Mobile | Falha | Sim |
| 9.4.2 Consistência Visual Desktop | Atencao | Não |
| 9.4.3 Estados Vazios | Atencao | Não |
| 9.4.4 Mensagens Django CRUD | Falha | Sim |
| 9.4.5 URLs e Navegação | Atencao | Não |

## Problemas críticos confirmados

**P1.1 — Sidebar fixa bloqueia mobile** (`templates/base_authenticated.html`)
Sidebar `w-64 fixed h-full` + main `ml-64` sem breakpoints responsivos. Em 375px a sidebar ocupa 68% da tela e não colapsa. Sem hamburguer, sem overlay, sem alternativa.

**P4.1 — Nenhum feedback visual após CRUD** (`accounts/views.py`, `categories/views.py`, `transactions/views.py`)
Todas as views CRUD usam AJAX com `JsonResponse({'success': True})` + `window.location.reload()`. O reload apaga flash messages. O usuário não recebe confirmação visual.

**P5.3/P2.4 — ProfileUpdateView sem GET** (`profiles/views.py`)
Herda de `View` e implementa apenas `post()`. GET para `/perfil/editar/` retorna 405 Method Not Allowed.

## Problemas médios confirmados

- P1.3: Tabelas sem `overflow-x-auto` em 3 templates de listagem
- P1.4: Grid do perfil com `style="grid-template-columns: 220px 1fr"` inline
- P3.1: Empty state de categorias por tipo abre `/categorias/nova/` em vez de `openCategoryModal()`
- P5.1: Rotas `/nova/` são endpoints órfãos não linkados na UI principal

## Problemas baixos confirmados

- P2.1: Saldo de conta sempre `text-emerald-400` mesmo quando negativo
- P2.3: Logo "Finanpy" não clicável nas páginas de login e cadastro (span, não anchor)
- P3.2: `recent_transactions` no dashboard sem `.order_by('-date')`
- P5.5: Perfil acessível apenas pelo dropdown, não pela sidebar

## Veredito MVP

Sistema **não pronto** para produção. Dois bloqueadores: ausência de responsividade mobile (P1.1) e ausência de feedback após CRUD (P4.1/P4.2).

**Why:** QA completa de design e visual antes de release MVP.
**How to apply:** Priorizar P1.1 e P4.1 antes de qualquer release.
