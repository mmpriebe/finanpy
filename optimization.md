# Auditoria Técnica — Finanpy

**Data:** 22/06/2026 | **Auditor:** Claude Sonnet 4.6 | **Revisão:** Profissional

---

## 1. Arquitetura e Qualidade de Código

### Pontos positivos

A estrutura está sólida: 6 apps com responsabilidades claras, CBV em todo lugar, isolamento de dados consistente via `filter(user=request.user)`, e padrão de signals para auto-criação de perfil feito corretamente com `dispatch_uid`.

### Problemas encontrados

---

#### 1.1 — `INPUT_CLASS` duplicado em 4 arquivos
**Localização:** `accounts/forms.py:5`, `categories/forms.py:5`, `profiles/forms.py:8`, `transactions/forms.py:7`
**Impacto:** Qualquer mudança no design system exige editar 4 arquivos. Já há inconsistência: `INPUT_CLASSES` (plural) em accounts/categories, `_INPUT` em profiles, `INPUT_CLASS` (sem `ES`) em transactions.
**Severidade:** Baixa
**Correção:** Criar `core/forms.py` com a constante compartilhada e importar nos 4 forms.

---

#### 1.2 — Método `_is_ajax()` duplicado em 6 views
**Localização:** `accounts/views.py:38,63`, `categories/views.py:28,50`, `transactions/views.py:71,98`
**Impacto:** O mesmo método de 1 linha duplicado 6 vezes. O padrão completo de AJAX (form_valid/form_invalid retornando JsonResponse) repete-se identicamente.
**Severidade:** Baixa
**Correção:** Um `AjaxFormMixin` que implemente `_is_ajax()`, `form_valid` e `form_invalid`, herdado por todas as views com formulário.

---

#### 1.3 — `get_queryset()` chamado duas vezes em `TransactionListView`
**Localização:** `transactions/views.py:60`

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)  # chama get_queryset() internamente
    ...
    qs = self.get_queryset()  # chama de novo, re-aplica todos os filtros
    context['income_count'] = qs.filter(...).count()
    context['expense_count'] = qs.filter(...).count()
```

**Impacto:** 3 queries desnecessárias a cada carregamento da lista de transações.
**Severidade:** Média
**Correção:** Usar `self.object_list` (já disponível após `super().get_context_data()`).

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    qs = self.object_list  # queryset já avaliado
    context['income_count'] = qs.filter(transaction_type='income').count()
    context['expense_count'] = qs.filter(transaction_type='expense').count()
    return context
```

---

#### 1.4 — `AccountListView` executa 5+ queries desnecessárias
**Localização:** `accounts/views.py:23-30`

```python
qs = self.get_queryset()       # 2ª chamada (já rodou para object_list)
active_qs = qs.filter(...)
context['active_count'] = active_qs.count()        # query 1
context['inactive_count'] = qs.filter(...).count() # query 2
context['total_balance'] = active_qs.aggregate()   # query 3
context['grand_total'] = qs.aggregate()            # query 4
```

**Severidade:** Média
**Correção:** Usar `self.object_list` e calcular tudo com `list()` ou uma única query com `values`.

---

#### 1.5 — `greeting` calculado duas vezes por request no Dashboard
**Localização:** `core/context_processors.py:11` e `core/views.py:128`
O context processor `finance_globals` já injeta `greeting`. A `DashboardView.get_context_data()` injeta novamente. O valor do view sobrescreve o do CP, mas ambos executam.
**Severidade:** Baixa
**Correção:** Remover `'greeting': _build_greeting(user)` de `DashboardView.get_context_data()`.

---

#### 1.6 — Filtro `by_type` faz iteração Python em vez de filtro de queryset
**Localização:** `accounts/templatetags/finance_filters.py:15`

```python
return [item for item in queryset if item.transaction_type == transaction_type]
```

**Impacto:** Se o queryset tiver centenas de categorias, itera todos em Python. Perde lazy evaluation.
**Severidade:** Baixa
**Correção:**

```python
try:
    return queryset.filter(transaction_type=transaction_type)
except AttributeError:
    return [item for item in queryset if item.transaction_type == transaction_type]
```

---

#### 1.7 — URL hardcoded no `RegisterView`
**Localização:** `users/views.py:12`

```python
success_url = '/dashboard/'  # deveria ser reverse_lazy('dashboard')
```

**Severidade:** Baixa
**Correção:** `success_url = reverse_lazy('dashboard')`

---

#### 1.8 — `except Exception: return {}` silencia erros no context processor
**Localização:** `core/context_processors.py:12`
Qualquer exceção — inclusive erros de programação — é silenciada e retorna um dict vazio. O template falha silenciosamente, dificultando debugging.
**Severidade:** Média
**Correção:**

```python
import logging
logger = logging.getLogger(__name__)

except Exception:
    logger.exception('Erro no context processor finance_globals')
    return {}
```

---

#### 1.9 — `TransactionDeleteView.form_valid` busca o objeto duas vezes
**Localização:** `transactions/views.py:131`

```python
def form_valid(self, form):
    self.object = self.get_object()  # query extra — Django já o tem
    self.object.delete()
```

`DeleteView` do Django já popula `self.object` antes de `form_valid`. A chamada extra a `get_object()` é desnecessária.
**Severidade:** Baixa

---

#### 1.10 — `balance` em `Account` é estático, não derivado de transações
**Localização:** `accounts/models.py:22`
O `balance` é editado manualmente. Não há signal ou mecanismo que ajuste o saldo ao criar/editar/deletar transações. O saldo da conta pode divergir das transações registradas ao longo do tempo.
**Severidade:** Alta
**Correção:** Definir uma estratégia clara — ou o saldo é sempre calculado via `Transaction.objects.filter(account=self).aggregate(...)`, ou signals atualizam `balance` a cada operação de transação.

---

#### 1.11 — Apps registrados de forma inconsistente em `INSTALLED_APPS`
**Localização:** `core/settings.py:42-47`
`profiles` usa `'profiles.apps.ProfilesConfig'` (correto, carrega signals via `ready()`). Os demais apps usam a forma curta `'accounts'`, `'categories'` etc. Se algum desses apps ganhar signals no futuro, eles não serão carregados automaticamente.
**Severidade:** Baixa
**Correção:** Registrar todos os apps com `AppConfig` explícito.

---

## 2. Segurança

---

#### 2.1 — `SECRET_KEY` com fallback inseguro hardcoded
**Localização:** `core/settings.py:23`

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-qjf=sv7n$qhb...')
```

Se implantado sem a env var, usa chave conhecida/previsível. Sessions, CSRF tokens e assinaturas ficam comprometidos.
**Risco:** Crítico
**Correção:**

```python
import sys

_secret = os.environ.get('SECRET_KEY')
if not _secret:
    if not DEBUG:
        sys.exit('SECRET_KEY não configurado em produção.')
    _secret = 'django-insecure-dev-only'
SECRET_KEY = _secret
```

---

#### 2.2 — `DEBUG` defaults to `True`
**Localização:** `core/settings.py:25`

```python
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

Se implantado sem a env var `DEBUG=False`, o Django exibe stack traces completos com variáveis de ambiente, settings e código-fonte para qualquer erro.
**Risco:** Alto
**Correção:**

```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

---

#### 2.3 — Cabeçalhos de segurança HTTP ausentes
**Localização:** `core/settings.py` — ausência de configurações

As seguintes configurações estão ausentes:

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Risco:** Alto (em produção sem HTTPS)

---

#### 2.4 — Nenhum rate limiting nas rotas de autenticação
**Localização:** `users/urls.py`, `users/views.py`
`/login/` e `/registro/` não têm rate limiting. Um atacante pode tentar senhas em larga escala sem bloqueio.
**Risco:** Alto
**Correção:**

```bash
pip install django-axes
```

```python
# settings.py
INSTALLED_APPS += ['axes']
MIDDLEWARE += ['axes.middleware.AxesMiddleware']
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hora
```

---

#### 2.5 — Sem verificação de e-mail no cadastro
**Localização:** `users/views.py:14-17`
Usuário pode cadastrar qualquer e-mail sem confirmação. Risco de registro com e-mail de terceiros e dados de usuário desvinculados do dono real.
**Risco:** Médio
**Correção:** Implementar fluxo de verificação com `django-allauth` ou token manual via `django.core.signing`.

---

#### 2.6 — Sem fluxo de recuperação de senha
**Localização:** Ausente no projeto
Usuário que esquece a senha perde acesso permanente à conta.
**Risco:** Alto (funcional — bloqueio crítico de usuário)
**Correção:** Implementar as URLs padrão do Django Auth:

```python
# users/urls.py
path('esqueci-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('esqueci-senha/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('redefinir/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('redefinir/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
```

---

#### 2.7 — `Transaction.amount` sem validação de valor positivo
**Localização:** `transactions/models.py:27`

```python
amount = models.DecimalField(max_digits=12, decimal_places=2)
```

Aceita valores negativos sem restrição no modelo.
**Risco:** Baixo
**Correção:**

```python
from decimal import Decimal
from django.core.validators import MinValueValidator

amount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    validators=[MinValueValidator(Decimal('0.01'))],
)
```

---

#### 2.8 — Formulário de telefone sem validação de formato
**Localização:** `profiles/forms.py:30`
Campo `phone` aceita qualquer string de até 20 caracteres sem validação de formato telefônico.
**Risco:** Baixo
**Correção:** Adicionar `RegexValidator` ou usar `django-phonenumber-field`.

---

## 3. Banco de Dados

---

#### 3.1 — Sem índices explícitos nos campos de filtro mais usados
**Localização:** `transactions/models.py`
Os campos `date`, `transaction_type` e o par `(user, date)` são usados em praticamente toda query de transação. Nenhum tem `db_index=True`.
**Impacto:** Com poucos registros imperceptível; com 10k+ transações, queries sem índice fazem full table scan.
**Correção:**

```python
date = models.DateField(db_index=True)
transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, db_index=True)

class Meta:
    ordering = ['-date', '-created_at']
    indexes = [
        models.Index(fields=['user', 'date'], name='transaction_user_date_idx'),
        models.Index(fields=['user', 'transaction_type', 'date'], name='transaction_type_date_idx'),
    ]
```

---

#### 3.2 — Falta de `select_related` nas queries com FK
**Localização:** `core/views.py:101-104`, templates de transações
`recent_transactions` no dashboard busca 5 transações sem `select_related`. No template, ao acessar `transaction.account.name` e `transaction.category.name`, Django faz 2 queries adicionais por transação — 10 queries extras para 5 transações.
**Severidade:** Média
**Correção:**

```python
recent_transactions = (
    Transaction.objects
    .filter(user=user)
    .select_related('account', 'category')
    .order_by('-date', '-created_at')[:5]
)
```

O mesmo se aplica a `TransactionListView.get_queryset()`.

---

#### 3.3 — SQLite em produção
**Localização:** `core/settings.py:84-89`
SQLite não suporta escrita concorrente — uma segunda request de escrita durante uma transação ativa resulta em `OperationalError: database is locked`. Para uso pessoal mono-usuário funciona; para múltiplos usuários simultâneos, falha.
**Severidade:** Alta (se a intenção é SaaS)
**Correção:** PostgreSQL via `psycopg2`. O `docker-compose.yml` já existe — adicionar um serviço Postgres é trivial.

---

#### 3.4 — `balance` de Account não reflete soma das transações
Ver item 1.10. A inconsistência de dados é um risco de integridade real que cresce com o tempo de uso.

---

## 4. Performance

| Gargalo | Localização | Impacto | Solução |
|---|---|---|---|
| N+1 em recent_transactions | `core/views.py:101` | 10+ queries por dashboard | `select_related('account', 'category')` |
| N+1 em transaction_list | `transactions/views.py:18` | N×2 queries por página | `select_related` no queryset |
| Context processor em toda request | `core/context_processors.py` | 2 queries em cada página | Cache por sessão ou low-level cache |
| `get_queryset()` duplo | `transactions/views.py:60` | 3 queries extras | Usar `self.object_list` |
| `get_queryset()` duplo | `accounts/views.py:25` | 4 queries extras | Usar `self.object_list` |
| Sem paginação | `transactions/views.py` | Load completo com 10k+ registros | `paginate_by = 50` |
| Sem índices no banco | `transactions/models.py` | Full table scan crescente | Índices compostos |
| `by_type` em Python | `finance_filters.py:15` | Iteração Python desnecessária | `.filter()` no queryset |

---

## 5. UX e Interface

### Pontos positivos

- Design system consistente e bonito (dark mode, paleta violet/indigo)
- Modais para criação/edição sem troca de página
- Empty states bem implementados
- Sidebar recolhível com localStorage
- Feedback de saudação contextual por horário

### Melhorias necessárias

**Crítico:**
- Sem fluxo de recuperação de senha — usuário bloqueado permanentemente
- Sem mensagem de erro amigável ao tentar excluir conta/categoria com transações vinculadas (`PROTECT` lança `ProtectedError` não tratado)

**Alto:**
- Sem paginação na lista de transações — com muitos lançamentos a página fica lenta e enorme
- Sem busca por descrição de transação
- Dashboard sem filtro de período — sempre exibe o mês atual
- Sem onboarding — novo usuário vê dashboard vazio sem orientação

**Médio:**
- Filtros de transação exigem digitar mês/ano manualmente — botões "Mês anterior", "Este mês", "Este ano" seriam muito mais práticos
- Campos de telefone e CEP sem máscara de input
- Formulário de cadastro não foca o primeiro campo automaticamente (`autofocus`)

**Baixo:**
- Sem indicação de força de senha no cadastro
- Nenhum modo claro (dark-only pode ser limitante para parte dos usuários)

---

## 6. Funcionalidades Existentes

| Funcionalidade | Status | Observações |
|---|---|---|
| Cadastro por e-mail | ✅ Completo | Sem verificação de e-mail |
| Login por e-mail | ✅ Completo | Sem rate limiting |
| Logout | ✅ Completo | — |
| Recuperação de senha | ❌ Ausente | **Funcionalidade crítica** |
| Verificação de e-mail | ❌ Ausente | — |
| Alteração de e-mail | ❌ Ausente | — |
| Alteração de senha | ❌ Ausente | — |
| Perfil pessoal | ✅ Completo | Nome, telefone |
| Endereço no perfil | ✅ Completo | — |
| Contas bancárias (CRUD) | ✅ Completo | 5 tipos de conta |
| Ativar/desativar conta | ✅ Completo | Toggle |
| Categorias (CRUD) | ✅ Completo | Receita e Despesa |
| Ativar/desativar categoria | ✅ Completo | Toggle |
| Transações (CRUD) | ✅ Completo | Com filtros |
| Filtros de transações | ✅ Parcial | Mês, ano, conta, categoria — sem busca por texto |
| Dashboard com métricas | ✅ Completo | Saldo total, receitas, despesas, taxa de poupança |
| Top categorias de despesa | ✅ Completo | Apenas mês atual |
| Paginação | ❌ Ausente | Risco de performance |
| Busca por descrição | ❌ Ausente | — |
| Exportar dados (CSV/PDF) | ❌ Ausente | — |
| Transferência entre contas | ❌ Ausente | — |
| Transações recorrentes | ❌ Ausente | — |
| Orçamento por categoria | ❌ Ausente | — |
| Metas financeiras | ❌ Ausente | — |
| Relatórios avançados | ❌ Ausente | Só dashboard básico |
| Importar CSV/OFX | ❌ Ausente | — |
| Admin configurado | ✅ Presente | Via Django admin |

---

## 7. Novas Funcionalidades Sugeridas

### Básicas — o que qualquer sistema financeiro moderno deve ter

| Funcionalidade | Benefício | Complexidade | Prioridade |
|---|---|---|---|
| Recuperação de senha | Usuário não perde acesso | Baixa | **Urgente** |
| Paginação na listagem | Performance e usabilidade | Baixa | **Urgente** |
| Busca por descrição de transação | Localizar lançamentos rapidamente | Baixa | Alta |
| Exportar para CSV | Backup e análise em planilhas | Baixa | Alta |
| Filtros de período rápidos | "Este mês", "Mês anterior", "Este ano" | Baixa | Alta |
| Transferência entre contas | Movimentação sem distorcer saldo | Média | Alta |
| Alteração de senha | Segurança básica de conta | Baixa | Alta |
| Tratar erro PROTECT | Mensagem amigável ao excluir conta com transações | Baixa | Alta |
| Saldo calculado por transações | Integridade financeira real | Média | Média |

### Intermediárias — agregam valor real

| Funcionalidade | Benefício | Complexidade | Prioridade |
|---|---|---|---|
| Transações recorrentes | Automatizar contas fixas (aluguel, salário) | Média | Alta |
| Orçamento por categoria | Controle de gastos com meta mensal | Média | Alta |
| Dashboard multi-período | Comparar meses, trimestres, anos | Média | Média |
| Gráfico de evolução de saldo | Visualizar tendência ao longo do tempo | Média | Média |
| Metas financeiras | Reserva de emergência, viagem, compra | Média | Média |
| Exportar PDF (extrato) | Extrato formatado para compartilhar | Média | Média |
| Importar CSV | Trazer histórico de outros sistemas/bancos | Alta | Média |
| Tags em transações | Classificação livre além das categorias | Baixa | Baixa |
| Notificações no browser | Lembretes de contas a pagar | Média | Baixa |

### Avançadas — diferenciais competitivos

| Funcionalidade | Benefício | Complexidade | Prioridade |
|---|---|---|---|
| Importar OFX/OFSL | Sincronizar com extrato bancário real | Alta | Alta |
| Relatórios comparativos | Este mês vs. mês anterior / ano anterior | Alta | Alta |
| Balanço patrimonial | Visão completa de patrimônio + dívidas | Alta | Média |
| Multi-moeda | Para quem tem contas em USD/EUR | Alta | Baixa |
| App mobile (PWA) | Acesso offline, adicionar transações no celular | Alta | Média |

### IA e Automação

| Funcionalidade | Descrição | Complexidade | Prioridade | Valor |
|---|---|---|---|---|
| Classificação automática | Ao digitar a descrição, sugere categoria com base no histórico | Média | Alta | Alto |
| Detecção de gastos anormais | Alerta quando despesa de categoria X supera média histórica | Média | Média | Alto |
| Previsão de fluxo de caixa | Projeta saldo dos próximos 30/60/90 dias com base em recorrências | Alta | Média | Alto |
| Assistente financeiro (chat) | Chat com IA que responde sobre as suas finanças ("Quanto gastei com alimentação em maio?") | Alta | Baixa | Muito Alto |
| Sugestão de economia | "Você gastou R$ 850 em delivery este mês — 40% acima da média" | Alta | Baixa | Alto |
| Categorização por foto de nota fiscal | Usuário tira foto da nota → IA extrai valor e categoria | Muito Alta | Baixa | Alto |

---

## 8. Monetização (SaaS)

### Estrutura de Planos Sugerida

**Plano Gratuito (Free)**
- 1 usuário
- Até 3 contas bancárias
- Até 5 categorias
- Histórico de 6 meses
- Dashboard básico
- Exportação limitada (últimas 50 transações)

**Plano Pessoal — R$ 14,90/mês**
- Contas e categorias ilimitadas
- Histórico completo
- Exportação CSV/PDF ilimitada
- Transações recorrentes
- Orçamento por categoria
- Metas financeiras

**Plano Pro — R$ 29,90/mês**
- Tudo do Pessoal
- Importação OFX/CSV de banco
- Classificação automática por IA
- Relatórios avançados (comparativo, tendências)
- Previsão de fluxo de caixa
- Multi-moeda

**Plano Família — R$ 39,90/mês**
- Até 5 contas de usuário
- Visão consolidada de gastos da família
- Categorias compartilhadas

### Estratégias de Retenção

- E-mail mensal com resumo financeiro ("Seu mês em números")
- Streaks de uso ("7 dias registrando transações")
- Alertas de orçamento proativos via e-mail/WhatsApp
- Relatório anual de finanças com insights ("Você economizou R$ 8.400 em 2025")
- Integração com WhatsApp para adicionar transação via mensagem

---

## 9. Roadmap

### Curto Prazo — 30 dias (Quick Wins)

1. **Recuperação de senha** — 4h, bloqueante para produção
2. **`DEBUG=False` por default e `SECRET_KEY` sem fallback inseguro** — 30min
3. **Rate limiting no login** (`django-axes`) — 2h
4. **Cabeçalhos de segurança HTTP** — 1h
5. **`select_related` nas queries de transações** — 2h
6. **Paginação na lista de transações** (`paginate_by = 50`) — 1h
7. **Corrigir dupla chamada de `get_queryset()`** — 2h
8. **Constante `INPUT_CLASS` centralizada** — 1h
9. **Mixin AJAX para views** — 2h
10. **Índices de banco de dados em Transaction** — 1h + migration

### Médio Prazo — 90 dias (Estrutural)

1. **Migrar para PostgreSQL** — arquitetura pronta para escala
2. **Fluxo de verificação de e-mail**
3. **Transferência entre contas** (com tipo especial de transação)
4. **Transações recorrentes** (model com `recurrence_rule`, `next_date`)
5. **Orçamento por categoria** (model `Budget` com limite mensal)
6. **Filtros de período rápidos** no frontend
7. **Busca por descrição** de transação
8. **Exportação CSV** do extrato filtrado
9. **Onboarding para novos usuários** (wizard de 3 passos)
10. **Tratamento de `ProtectedError`** com mensagem amigável
11. **Configurar logging** estruturado
12. **Alterar senha** via perfil
13. **Estratégia de saldo** — derivar de transações ou manter via signal

### Longo Prazo — 6 a 12 meses (Diferenciais)

1. **Importação OFX/CSV** de extratos bancários
2. **Classificação automática** via modelo local (TF-IDF nas descrições históricas)
3. **Dashboard multi-período** com gráficos de linha (Chart.js ou Apache ECharts)
4. **Previsão de fluxo de caixa** com base em recorrências
5. **Planos e cobrança** (Stripe via `dj-stripe`)
6. **PWA (Progressive Web App)** para uso mobile offline
7. **Assistente financeiro** (Claude API + RAG sobre as transações do usuário)
8. **Multi-tenancy** completo com isolamento por plano
9. **Notificações por e-mail** (Celery + django-celery-beat para agendamento)
10. **API REST** pública para integrações futuras (DRF)

---

## 10. Relatório Final

### Pontos Fortes

- Arquitetura limpa com apps bem delimitados e sem acoplamento cruzado desnecessário
- Isolamento de dados rigoroso — `filter(user=request.user)` aplicado consistentemente em toda view
- CBV como padrão universal, com `get_queryset` sobrescrito corretamente em UpdateView/DeleteView
- Design system coeso e bem executado — dark mode, paleta definida, componentes reutilizáveis
- Signal com `dispatch_uid` para auto-criação de perfil — implementação correta
- Template tags de filtro (`brl_currency`, `by_type`) centralizadas no app correto
- Uso correto de `PROTECT` em FK de transações — evita deleção acidental de dados referenciados
- `docker-compose.yml` presente — infraestrutura pronta para evoluir
- CLAUDE.md documentado — facilita onboarding

### Pontos Fracos

- Sem recuperação de senha — bloqueante para qualquer usuário real
- `SECRET_KEY` com fallback inseguro e `DEBUG=True` por default — perigoso em produção
- Sem rate limiting na autenticação — vulnerável a ataques de força bruta
- Cabeçalhos HTTP de segurança ausentes (HTTPS, HSTS, cookies seguros)
- `balance` de conta desvinculado das transações — inconsistência de dados garantida com o tempo
- N+1 queries em templates com transações — degradação de performance com crescimento
- Sem paginação — performance comprometida com dados reais de longo prazo
- Código duplicado: constante de input CSS (4x), método `_is_ajax()` (6x), padrão AJAX form (6x)
- Sem índices de banco de dados no campo `date` e `transaction_type` de transações
- SQLite inadequado para ambiente multi-usuário simultâneo
- `except Exception: return {}` no context processor silencia bugs reais

### Riscos Técnicos

- **Deploy acidental com `DEBUG=True` e `SECRET_KEY` insegura** — expõe código-fonte e invalida criptografia
- **Saldo inconsistente** — usuário pode ter saldo exibido diferente da soma real das transações ao longo do tempo
- **Bloqueio de usuário por senha esquecida** — sem recovery, usuário perde acesso permanentemente
- **`ProtectedError` sem tratamento** — ao excluir conta/categoria com transações, Django lança 500 não tratado
- **Escalabilidade de SQLite** — com 2+ usuários simultâneos escrevendo, risco de `database is locked`
- **Performance com dados reais** — sem paginação e sem `select_related`, 10k+ transações tornam a lista lenta

### Top 10 Melhorias por Impacto

| # | Melhoria | Impacto |
|---|---|---|
| 1 | Recuperação de senha | Usuários não ficam bloqueados permanentemente |
| 2 | `DEBUG=False` default + `SECRET_KEY` sem fallback inseguro | Segurança crítica de produção |
| 3 | Cabeçalhos HTTP de segurança (HTTPS, HSTS, cookies seguros) | Segurança em trânsito |
| 4 | Rate limiting no login (`django-axes`) | Proteção contra brute force |
| 5 | `select_related('account', 'category')` nas queries de transações | Elimina N+1, performance imediata |
| 6 | Paginação na lista de transações | UX e performance com dados reais |
| 7 | Tratamento de `ProtectedError` | Evita tela de erro 500 ao excluir entidades vinculadas |
| 8 | Índices compostos em `Transaction(user, date)` | Performance de queries à medida que dados crescem |
| 9 | Estratégia clara de saldo de conta | Integridade financeira dos dados |
| 10 | Migrar de SQLite para PostgreSQL | Viabilidade multi-usuário e escala |

---

### Nota Geral

| Dimensão | Nota | Justificativa |
|---|---|---|
| **Arquitetura** | 8.0/10 | Apps bem separados, CBV correto, isolamento de dados — perde por duplicação de código e saldo desvinculado |
| **Segurança** | 5.0/10 | CSRF ativo, isolamento de dados OK — porém SECRET_KEY fraca, DEBUG=True, sem rate limiting, sem HTTPS headers |
| **Performance** | 6.0/10 | Queries simples e eficientes para escala atual — N+1, sem paginação e sem índices são bombas-relógio |
| **Escalabilidade** | 5.5/10 | SQLite bloqueia escala, sem paginação, sem cache — boa base arquitetural mas infraestrutura limitante |
| **UX** | 7.5/10 | Design excelente, modais funcionais, empty states — falta recovery de senha, onboarding, busca |
| **Potencial Comercial** | 7.0/10 | Nicho claro, execução visual acima da média — faltam funcionalidades chave para cobrar de usuários reais |

**Nota Global: 6.5/10** — Código bem escrito para um MVP, com bom design e arquitetura sólida. Os gaps de segurança e as funcionalidades ausentes são resolvíveis em 30–90 dias de trabalho focado. O sistema tem base real para evoluir para um produto SaaS competitivo no mercado brasileiro.
