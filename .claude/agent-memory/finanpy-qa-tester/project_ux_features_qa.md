---
name: ux-features-qa-2026-06-22
description: QA dos recursos UX-01, UX-02, UX-03 (período rápido, busca por descrição, onboarding banner) — sessão 2026-06-22
metadata:
  type: project
---

Sessão de QA em 2026-06-22 cobrindo 3 novas funcionalidades implementadas.

**URL testada:** http://172.18.8.58:8000 (servidor externo, já em execução)
**Método:** análise estática completa dos templates e views (Playwright MCP indisponível na sessão)

## UX-03 — Banner de Onboarding (dashboard.html + core/views.py)

Implementação verificada e correta para todos os sub-casos:
- Condicional `{% if show_onboarding %}` em dashboard.html linha 187
- `show_onboarding = onboarding_steps_done < 3` calculado em core/views.py linha 142
- Progresso via `{% widthratio onboarding_steps_done 3 100 %}%` na linha 224
- Etapa 1 linka para `accounts:list`, etapa 2 para `categories:list` (correto)
- Etapa 3 usa `<div ... cursor-not-allowed opacity-50>` quando pré-requisitos faltam (linha 303)
- Dismiss via localStorage em bloco `<script>` (linhas 599-615): oculta o banner antes do carregamento se `finanpy_onboarding_dismissed === '1'`

**Bug conhecido (baixo):** O JS esconde o banner após o DOM carregar, causando flash de ~1 frame. Para eliminar, injetar `style="display:none"` via script inline ANTES do `<div id="onboarding-banner">`.

## UX-01 — Botões de Período Rápido (transaction_list.html linhas 472-492 e JS 808-868)

Implementação verificada e correta:
- 3 botões: `btn-este-mes`, `btn-mes-anterior`, `btn-este-ano`
- `setQuickPeriod()` popula month/year e chama `form.submit()`
- `highlightActive()` compara `currentMonth`/`currentYear` com valores do Django e aplica `bg-violet-600/20 border-violet-600/50 text-violet-400`
- "Este ano" define `monthSelect.value = ''` e `yearInput.value = String(thisYear)` — filtro correto
- "Limpar" navega para URL limpa via `<a href="{% url 'transactions:list' %}">` (linha 615)

**Sem bugs funcionais.** Comportamento esperado para janeiro → mês anterior = dezembro do ano anterior também está correto (linhas 813-814).

## UX-02 — Busca por Descrição (transaction_list.html linhas 581-601 e transactions/views.py linhas 50-52)

Implementação verificada e correta:
- Campo `<input type="search" name="q">` com ícone de lupa (linha 595)
- `value="{{ current_q }}"` mantém valor após submit
- Filtro na view: `qs.filter(description__icontains=q)` — case-insensitive
- Empty state diferenciado: `{% if current_q %}` exibe "Nenhuma transação encontrada para 'X'" (linha 787)
- "Limpar" (link sem params) remove busca junto com outros filtros

**Bug UX (médio):** `<input type="search">` em alguns browsers renderiza botão X nativo que limpa o campo sem resubmeter o form. Correção: adicionar `oninput="if(!this.value) this.form.submit()"` na linha 595 de transaction_list.html.

**Why:** O comportamento nativo de `type="search"` é inconsistente entre browsers — o X nativo limpa o campo visualmente mas não submete o form Django.
**How to apply:** Reportar este bug sempre que UX-02 for re-testado.

## Nota sobre empty state (transaction_list.html linhas 786-792)

A mensagem de empty state sem transações ("Registre sua primeira receita ou despesa") pode aparecer enganosamente para usuários que têm transações em outros períodos sem filtro ativo. Recomenda-se adicionar flag `user_has_any_transactions` no contexto da view para diferenciar o caso "usuário sem dados" do "sem resultado no filtro".
