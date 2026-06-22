# Optimization Tasks — Finanpy

Sprints e tarefas derivadas da auditoria técnica (`optimization.md`).
Ordenadas por impacto e dependência. Cada tarefa inclui os arquivos afetados e estimativa de esforço.

---

## Sprint 0 — Segurança Crítica (Esta semana)

> Itens que não devem entrar em produção sem estar resolvidos.

- [ ] **SEC-01** — Alterar default de `DEBUG` para `False`
  - Arquivo: `core/settings.py:25`
  - Mudança: `os.environ.get('DEBUG', 'False') == 'True'`
  - Esforço: 5 min

- [ ] **SEC-02** — Remover fallback inseguro de `SECRET_KEY`
  - Arquivo: `core/settings.py:23`
  - Mudança: levantar `sys.exit()` se `SECRET_KEY` não estiver definida e `DEBUG=False`
  - Esforço: 15 min

- [ ] **SEC-03** — Adicionar cabeçalhos HTTP de segurança
  - Arquivo: `core/settings.py`
  - Adicionar: `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_CONTENT_TYPE_NOSNIFF`
  - Esforço: 30 min

- [ ] **SEC-04** — Corrigir `DEBUG` default no `.env.example`
  - Arquivo: `.env.example`
  - Garantir que o exemplo mostre `DEBUG=False` e `SECRET_KEY=<gere-uma-chave>`
  - Esforço: 10 min

---

## Sprint 1 — Correções de Código (Semana 1–2)

> Bugs, duplicações e inconsistências identificados na auditoria.

### Qualidade de código

- [ ] **COD-01** — Centralizar constante de input CSS
  - Criar: `core/forms.py` com `INPUT_CLASS = '...'`
  - Remover duplicatas de: `accounts/forms.py`, `categories/forms.py`, `profiles/forms.py`, `transactions/forms.py`
  - Esforço: 30 min

- [ ] **COD-02** — Criar `AjaxFormMixin` para eliminar duplicação de AJAX handling
  - Criar: `core/mixins.py` com `AjaxFormMixin` implementando `_is_ajax()`, `form_valid`, `form_invalid`
  - Atualizar: `accounts/views.py`, `categories/views.py`, `transactions/views.py`
  - Esforço: 1h

- [ ] **COD-03** — Corrigir dupla chamada de `get_queryset()` em `TransactionListView`
  - Arquivo: `transactions/views.py:60`
  - Mudança: substituir `self.get_queryset()` por `self.object_list` em `get_context_data`
  - Esforço: 15 min

- [ ] **COD-04** — Corrigir dupla chamada de `get_queryset()` em `AccountListView`
  - Arquivo: `accounts/views.py:25`
  - Mudança: substituir `self.get_queryset()` por `self.object_list` em `get_context_data`
  - Esforço: 15 min

- [ ] **COD-05** — Remover `greeting` duplicado do `DashboardView`
  - Arquivo: `core/views.py:128`
  - Mudança: remover `'greeting': _build_greeting(user)` — já injetado pelo context processor
  - Esforço: 5 min

- [ ] **COD-06** — Corrigir `success_url` hardcoded no `RegisterView`
  - Arquivo: `users/views.py:12`
  - Mudança: `success_url = reverse_lazy('dashboard')`
  - Esforço: 5 min

- [ ] **COD-07** — Adicionar logging no context processor
  - Arquivo: `core/context_processors.py:12`
  - Mudança: substituir `except Exception: return {}` por log em nível WARNING
  - Esforço: 10 min

- [ ] **COD-08** — Corrigir query dupla em `TransactionDeleteView.form_valid`
  - Arquivo: `transactions/views.py:131`
  - Mudança: remover `self.object = self.get_object()` — `self.object` já está populado pelo Django
  - Esforço: 5 min

- [ ] **COD-09** — Corrigir filtro `by_type` para usar queryset em vez de iteração Python
  - Arquivo: `accounts/templatetags/finance_filters.py:15`
  - Mudança: usar `.filter(transaction_type=transaction_type)` quando possível
  - Esforço: 15 min

- [ ] **COD-10** — Padronizar registro dos apps em `INSTALLED_APPS` com `AppConfig`
  - Arquivo: `core/settings.py:42-47`
  - Mudança: registrar `accounts`, `categories`, `transactions`, `users` com sua `AppConfig` explícita
  - Esforço: 30 min

---

## Sprint 2 — Performance e Banco de Dados (Semana 2–3)

> Queries N+1, índices ausentes e paginação.

- [ ] **PERF-01** — Adicionar `select_related` em `recent_transactions` no dashboard
  - Arquivo: `core/views.py:101`
  - Mudança: `.select_related('account', 'category')` na query
  - Esforço: 10 min

- [ ] **PERF-02** — Adicionar `select_related` em `TransactionListView.get_queryset`
  - Arquivo: `transactions/views.py:19`
  - Mudança: `.select_related('account', 'category')` na query base
  - Esforço: 10 min

- [ ] **PERF-03** — Adicionar paginação na lista de transações
  - Arquivo: `transactions/views.py`
  - Mudança: `paginate_by = 50` na `TransactionListView`
  - Atualizar: `templates/transactions/transaction_list.html` com controles de paginação
  - Esforço: 1h

- [ ] **PERF-04** — Adicionar índices compostos no model `Transaction`
  - Arquivo: `transactions/models.py`
  - Adicionar: `db_index=True` em `date` e `transaction_type`; `Meta.indexes` com `(user, date)` e `(user, transaction_type, date)`
  - Gerar migration: `python manage.py makemigrations transactions`
  - Esforço: 30 min + migration

- [ ] **PERF-05** — Adicionar validação de valor positivo em `Transaction.amount`
  - Arquivo: `transactions/models.py:27`
  - Adicionar: `MinValueValidator(Decimal('0.01'))`
  - Gerar migration: `python manage.py makemigrations transactions`
  - Esforço: 20 min + migration

- [ ] **PERF-06** — Investigar e definir estratégia de saldo de Account
  - Arquivos: `accounts/models.py`, `transactions/models.py`
  - Opção A: signal `post_save`/`post_delete` em `Transaction` que recalcula `account.balance`
  - Opção B: property `balance` computada via `aggregate` (sem persistência)
  - Esforço: 2–4h dependendo da opção escolhida

---

## Sprint 3 — Segurança de Autenticação (Semana 3–4)

> Funcionalidades de segurança ausentes que bloqueiam uso em produção.

- [ ] **AUTH-01** — Implementar recuperação de senha
  - Arquivo: `users/urls.py`
  - Adicionar 4 URLs padrão do Django Auth (`PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, `PasswordResetCompleteView`)
  - Criar templates: `users/password_reset.html`, `users/password_reset_done.html`, `users/password_reset_confirm.html`, `users/password_reset_complete.html`
  - Configurar backend de e-mail em `core/settings.py` (`EMAIL_BACKEND`, `EMAIL_HOST`, etc.)
  - Esforço: 4h

- [ ] **AUTH-02** — Implementar alteração de senha via perfil
  - Arquivo: `profiles/views.py`, `profiles/urls.py`
  - Usar `PasswordChangeView` do Django Auth
  - Criar template: `profiles/password_change.html`
  - Esforço: 2h

- [ ] **AUTH-03** — Adicionar link "Esqueci minha senha" na tela de login
  - Arquivo: `templates/users/login.html`
  - Adicionar link apontando para `password_reset`
  - Esforço: 15 min (depende de AUTH-01)

- [ ] **AUTH-04** — Instalar e configurar `django-axes` para rate limiting
  - Arquivo: `core/settings.py`, `requirements.txt`
  - `pip install django-axes`
  - Configurar: `AXES_FAILURE_LIMIT = 5`, `AXES_COOLOFF_TIME = 1`
  - Adicionar middleware: `axes.middleware.AxesMiddleware`
  - Esforço: 1h

- [ ] **AUTH-05** — Adicionar validação de formato no campo `phone` do perfil
  - Arquivo: `profiles/forms.py`
  - Adicionar `RegexValidator` com padrão `^\(\d{2}\) \d{4,5}-\d{4}$`
  - Esforço: 20 min

- [ ] **AUTH-06** — Tratar `ProtectedError` ao excluir Account ou Category com transações
  - Arquivos: `accounts/views.py`, `categories/views.py`
  - Sobrescrever `delete()` ou usar `try/except ProtectedError` para exibir mensagem amigável
  - Esforço: 1h

---

## Sprint 4 — UX e Navegação (Semana 4–6)

> Melhorias de experiência que aumentam retenção e usabilidade.

- [x] **UX-01** — Adicionar botões de período rápido nos filtros de transações
  - Arquivo: `templates/transactions/transaction_list.html`
  - Adicionar: botões "Este mês", "Mês anterior", "Este ano" que preenchem os filtros via JavaScript
  - Esforço: 2h

- [x] **UX-02** — Implementar busca por descrição de transação
  - Arquivo: `transactions/views.py:TransactionListView.get_queryset`
  - Adicionar parâmetro `q` na query string: `qs.filter(description__icontains=q)`
  - Arquivo: `templates/transactions/transaction_list.html` — campo de busca no topo
  - Esforço: 1h

- [x] **UX-03** — Adicionar onboarding para novos usuários
  - Arquivos: `templates/dashboard.html`, `core/views.py`
  - Lógica: se usuário não tem contas ou categorias, exibir banner/wizard de primeiros passos
  - Esforço: 3h

- [ ] **UX-04** — Adicionar máscara de input para telefone e CEP
  - Arquivo: `templates/profiles/profile_detail.html`
  - Usar biblioteca leve de máscara (IMask.js ou similar via CDN)
  - Esforço: 1h

- [ ] **UX-05** — Adicionar `autofocus` no primeiro campo dos formulários de login e cadastro
  - Arquivos: `templates/users/login.html`, `templates/users/register.html`
  - Mudança: adicionar atributo `autofocus` no input de e-mail
  - Esforço: 10 min

- [ ] **UX-06** — Exibir mensagem amigável quando não há transações no período filtrado
  - Arquivo: `templates/transactions/transaction_list.html`
  - Condição: filtro aplicado + lista vazia → mensagem contextual diferente do empty state padrão
  - Esforço: 30 min

- [ ] **UX-07** — Indicador de força de senha no cadastro
  - Arquivo: `templates/users/register.html`
  - Implementar barra de força de senha com JavaScript puro (sem lib)
  - Esforço: 2h

---

## Sprint 5 — Exportação e Relatórios (Semana 6–8)

- [ ] **REL-01** — Exportar transações para CSV
  - Criar: `transactions/views.py:TransactionExportView`
  - Usar `csv.writer` da stdlib — sem dependências extras
  - Respeitar filtros ativos (mês, ano, conta, categoria)
  - Adicionar URL: `transacoes/exportar/`
  - Adicionar botão na `transaction_list.html`
  - Esforço: 2h

- [ ] **REL-02** — Dashboard com seletor de período (não só mês atual)
  - Arquivo: `core/views.py:DashboardView`
  - Aceitar parâmetros `month` e `year` via GET
  - Adicionar seletor de mês/ano no `templates/dashboard.html`
  - Esforço: 3h

- [ ] **REL-03** — Relatório mensal: comparativo mês atual vs. mês anterior
  - Arquivo: `core/views.py:DashboardView`
  - Calcular deltas percentuais de receita, despesa e saldo
  - Exibir indicadores de variação nos cards do dashboard
  - Esforço: 2h

---

## Sprint 6 — Funcionalidades Financeiras Intermediárias (Semana 8–14)

- [ ] **FIN-01** — Transferência entre contas
  - Criar model `Transfer` (ou tratar como par de transações vinculadas)
  - Criar views: `TransferCreateView`
  - Criar template: `transactions/transfer_form.html`
  - Lógica: débito na conta origem + crédito na conta destino em uma transação atômica (`transaction.atomic()`)
  - Esforço: 6h

- [ ] **FIN-02** — Orçamento por categoria
  - Criar app `budgets` (ou model `Budget` no app `categories`)
  - Campos: `user`, `category`, `month`, `year`, `limit_amount`
  - Dashboard: barra de progresso por categoria mostrando gasto vs. orçamento
  - Esforço: 8h

- [ ] **FIN-03** — Transações recorrentes
  - Criar model `RecurringTransaction` com campos: `frequency` (mensal, semanal, anual), `next_date`, `end_date`
  - Criar management command `generate_recurring` para executar via cron
  - Criar views e template para gerenciar recorrências
  - Esforço: 12h

- [ ] **FIN-04** — Metas financeiras
  - Criar app `goals`
  - Campos: `name`, `target_amount`, `current_amount`, `deadline`, `account` (opcional)
  - Dashboard: card de progresso de metas
  - Esforço: 8h

---

## Sprint 7 — Infraestrutura e Escala (Semana 6–10, paralela)

- [ ] **INFRA-01** — Migrar de SQLite para PostgreSQL
  - Atualizar `docker-compose.yml`: adicionar serviço `db` (postgres:16)
  - Atualizar `core/settings.py`: usar `dj-database-url` ou configuração direta
  - Atualizar `requirements.txt`: adicionar `psycopg2-binary`
  - Testar migrations em banco limpo
  - Esforço: 3h

- [ ] **INFRA-02** — Configurar variáveis de ambiente com `python-decouple` ou `django-environ`
  - Arquivo: `core/settings.py`, `requirements.txt`, `.env.example`
  - Centralizar toda configuração sensível em `.env`
  - Esforço: 1h

- [ ] **INFRA-03** — Configurar logging estruturado
  - Arquivo: `core/settings.py`
  - Adicionar configuração `LOGGING` com handlers para console e arquivo
  - Nível: WARNING em produção, DEBUG em desenvolvimento
  - Esforço: 1h

- [ ] **INFRA-04** — Configurar cache para context processor `finance_globals`
  - Arquivo: `core/context_processors.py`
  - Usar Django per-request cache ou cache de sessão para evitar 2 queries em toda página
  - Esforço: 1h

- [ ] **INFRA-05** — Configurar Celery + django-celery-beat para tarefas assíncronas
  - Necessário para: e-mails de recuperação de senha, transações recorrentes, notificações
  - Atualizar `docker-compose.yml` com serviço `redis` e `celery`
  - Esforço: 4h

---

## Sprint 8 — Longo Prazo: IA e Automação (3–6 meses)

- [ ] **AI-01** — Classificação automática de transações por categoria
  - Coletar histórico de descrições + categorias do usuário
  - Implementar modelo simples TF-IDF + KNN (sklearn) ou chamar Claude API
  - Retornar sugestão de categoria no formulário de nova transação via AJAX
  - Esforço: 12h

- [ ] **AI-02** — Detecção de gastos anormais
  - Calcular média histórica por categoria (últimos 6 meses)
  - Gerar alerta quando gasto do mês superar 150% da média
  - Exibir alertas no dashboard e/ou enviar e-mail
  - Esforço: 8h

- [ ] **AI-03** — Previsão de fluxo de caixa (30/60/90 dias)
  - Usar recorrências cadastradas + média histórica por categoria
  - Projetar saldo futuro em gráfico de linha
  - Esforço: 16h

- [ ] **AI-04** — Assistente financeiro via chat (Claude API)
  - Endpoint: `/assistente/` com interface de chat
  - RAG: buscar transações do usuário como contexto antes de chamar a API
  - Responder perguntas como "Quanto gastei com alimentação em maio?" ou "Estou no caminho certo para minha meta?"
  - Esforço: 20h

- [ ] **AI-05** — Categorização por foto de nota fiscal
  - Aceitar upload de imagem no formulário de transação
  - Chamar Claude API com `vision` para extrair valor, data, estabelecimento e categoria
  - Pré-preencher o formulário com os dados extraídos
  - Esforço: 12h

---

## Sprint 9 — Longo Prazo: SaaS e Monetização (6–12 meses)

- [ ] **SAAS-01** — Implementar sistema de planos com `dj-stripe`
  - Definir planos Free, Pessoal, Pro, Família
  - Criar middleware de verificação de plano antes de features premium
  - Criar tela de upgrade com integração Stripe Checkout
  - Esforço: 20h

- [ ] **SAAS-02** — Importação de extrato OFX/CSV
  - Aceitar upload de arquivo OFX (Open Financial Exchange) ou CSV genérico
  - Parser de OFX: `ofxparse` ou implementação própria
  - Tela de mapeamento de colunas (para CSV)
  - Detectar duplicatas antes de importar
  - Esforço: 16h

- [ ] **SAAS-03** — PWA (Progressive Web App)
  - Criar `manifest.json` e `service-worker.js`
  - Habilitar instalação no celular e cache offline das páginas principais
  - Ícones e splash screen
  - Esforço: 8h

- [ ] **SAAS-04** — E-mail mensal de resumo financeiro
  - Template de e-mail HTML com métricas do mês
  - Celery beat task no dia 1 de cada mês
  - Opt-in/opt-out no perfil do usuário
  - Esforço: 6h

- [ ] **SAAS-05** — API REST pública (DRF)
  - Instalar `djangorestframework`
  - Serializers e ViewSets para `Transaction`, `Account`, `Category`
  - Autenticação via Token
  - Documentação automática com `drf-spectacular`
  - Esforço: 16h

- [ ] **SAAS-06** — Verificação de e-mail no cadastro
  - Usar `django-allauth` ou implementar com `django.core.signing`
  - Enviar e-mail com link de confirmação ao registrar
  - Bloquear acesso até confirmação (ou apenas avisar)
  - Esforço: 4h

---

## Resumo por Sprint

| Sprint | Tema | Tarefas | Esforço estimado |
|---|---|---|---|
| Sprint 0 | Segurança Crítica | 4 | ~1h |
| Sprint 1 | Correções de Código | 10 | ~4h |
| Sprint 2 | Performance e BD | 6 | ~5h + migrations |
| Sprint 3 | Autenticação | 6 | ~9h |
| Sprint 4 | UX e Navegação | 7 | ~10h |
| Sprint 5 | Exportação e Relatórios | 3 | ~7h |
| Sprint 6 | Funcionalidades Financeiras | 4 | ~34h |
| Sprint 7 | Infraestrutura | 5 | ~10h |
| Sprint 8 | IA e Automação | 5 | ~68h |
| Sprint 9 | SaaS e Monetização | 6 | ~70h |
| **Total** | | **56 tarefas** | **~218h** |

---

## Dependências entre Tarefas

```
SEC-01, SEC-02 → pré-requisito para qualquer deploy em produção
AUTH-01 → AUTH-03 (link na tela de login)
INFRA-05 (Celery) → FIN-03 (recorrências), SAAS-04 (e-mail mensal)
FIN-01 (transferências) → PERF-06 (estratégia de saldo) deve estar definida antes
AI-03 (previsão) → FIN-03 (recorrências) como fonte de dados
SAAS-01 (planos) → qualquer feature premium
INFRA-01 (PostgreSQL) → SAAS-05 (API) — SQLite não é adequado para produção
```
